#!/usr/bin/env node

/**
 * Architecture fitness functions executed in CI.
 * Ensures coupling, performance, API changes, database safety,
 * SLO compliance, and security headers meet agreed standards.
 */

const assert = require("assert");
const fs = require("fs");
const path = require("path");

const madge = require("madge");
const yaml = require("js-yaml");

const DEFAULT_SRC_DIR = path.resolve("src");
const DEFAULT_DIST_DIR = path.resolve("dist");
const DEFAULT_MIGRATIONS_DIR = path.resolve("migrations");
const DEFAULT_PROMETHEUS_URL =
  process.env.PROMETHEUS_URL || "http://localhost:9090";
const DEFAULT_APP_URL = process.env.APP_URL || "http://localhost:3000";

const PERFORMANCE_BUDGETS = {
  "bundle.js": 170 * 1024,
  "bundle.css": 50 * 1024,
  "vendor.js": 300 * 1024,
};

const MIGRATION_WARN_PATTERNS = [
  /DROP\s+TABLE/i,
  /ALTER\s+TABLE.*DROP\s+COLUMN/i,
  /TRUNCATE/i,
];

const PROMETHEUS_QUERIES = {
  availability:
    '(sum(rate(http_requests_total{status=~"2.."}[30d])) / sum(rate(http_requests_total[30d]))) * 100',
  latency_p95:
    "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[30d])) by (le))",
  error_rate:
    '(sum(rate(http_requests_total{status=~"5.."}[30d])) / sum(rate(http_requests_total[30d]))) * 100',
};

const PROMETHEUS_SLOS = {
  availability: 99.9,
  latency_p95: 0.3,
  error_rate: 0.1,
};

const fetchCache = {
  client: typeof fetch === "function" ? fetch : null,
};

async function ensureFetch() {
  if (fetchCache.client) {
    return fetchCache.client;
  }

  const { default: nodeFetch } = await import("node-fetch");
  fetchCache.client = nodeFetch;
  return fetchCache.client;
}

async function checkCoupling({ srcDir = DEFAULT_SRC_DIR } = {}) {
  console.log("🔍 Checking dependency coupling");
  const result = await madge(srcDir);

  const circular = result.circular();
  assert.strictEqual(
    circular.length,
    0,
    `Found ${circular.length} circular dependencies: ${JSON.stringify(circular)}`,
  );

  const dependencies = result.obj();
  for (const [moduleId, deps] of Object.entries(dependencies)) {
    if (moduleId.includes("core/")) {
      const featureDeps = deps.filter((dep) => dep.includes("features/"));
      assert.strictEqual(
        featureDeps.length,
        0,
        `Core module ${moduleId} depends on feature modules: ${featureDeps.join(", ")}`,
      );
    }
  }

  console.log("✅ Coupling check passed");
}

function checkPerformanceBudgets({
  distDir = DEFAULT_DIST_DIR,
  budgets = PERFORMANCE_BUDGETS,
} = {}) {
  console.log("🔍 Checking performance budgets");

  for (const [asset, maxSize] of Object.entries(budgets)) {
    const filePath = path.join(distDir, asset);

    if (!fs.existsSync(filePath)) {
      console.log(`⚠️  Skipping ${asset} - file not found`);
      continue;
    }

    const stats = fs.statSync(filePath);
    const sizeKb = stats.size / 1024;
    const budgetKb = maxSize / 1024;

    assert.ok(
      stats.size <= maxSize,
      `File ${asset} is ${sizeKb.toFixed(2)}KB, exceeds budget of ${budgetKb.toFixed(2)}KB`,
    );

    console.log(
      `✅ ${asset}: ${sizeKb.toFixed(2)}KB (budget: ${budgetKb.toFixed(2)}KB)`,
    );
  }

  console.log("✅ Performance budgets met");
}

async function checkApiStability({
  currentSpecPath = path.resolve("openapi.yaml"),
  previousSpecPath = path.resolve("openapi-previous.yaml"),
} = {}) {
  console.log("🔍 Checking API contract stability");

  if (!fs.existsSync(currentSpecPath) || !fs.existsSync(previousSpecPath)) {
    throw new Error(
      "OpenAPI specs not found; ensure current and previous specs exist",
    );
  }

  const currentSpec = yaml.load(fs.readFileSync(currentSpecPath, "utf8"));
  const previousSpec = yaml.load(fs.readFileSync(previousSpecPath, "utf8"));

  const breakingChanges = [];

  for (const pathKey of Object.keys(previousSpec.paths || {})) {
    if (!currentSpec.paths?.[pathKey]) {
      breakingChanges.push(`Removed endpoint: ${pathKey}`);
    }
  }

  for (const [pathKey, methods] of Object.entries(currentSpec.paths || {})) {
    for (const [method, details] of Object.entries(methods)) {
      const previousDetails = previousSpec.paths?.[pathKey]?.[method];
      if (!previousDetails || !Array.isArray(details.parameters)) {
        continue;
      }

      const newRequired = details.parameters.filter(
        (parameter) =>
          parameter.required &&
          !previousDetails.parameters?.some(
            (prev) => prev.name === parameter.name,
          ),
      );

      if (newRequired.length > 0) {
        breakingChanges.push(
          `New required parameter in ${method.toUpperCase()} ${pathKey}: ${newRequired
            .map((param) => param.name)
            .join(", ")}`,
        );
      }
    }
  }

  assert.strictEqual(
    breakingChanges.length,
    0,
    `Breaking changes detected:\n${breakingChanges.join("\n")}`,
  );

  console.log("✅ API contract stability check passed");
}

function checkMigrations({
  migrationsDir = DEFAULT_MIGRATIONS_DIR,
  patterns = MIGRATION_WARN_PATTERNS,
} = {}) {
  console.log("🔍 Checking database migration safety");

  if (!fs.existsSync(migrationsDir)) {
    console.log(
      `⚠️  Migrations directory ${migrationsDir} not found; skipping`,
    );
    return;
  }

  const migrations = fs
    .readdirSync(migrationsDir)
    .filter((file) => file.endsWith(".sql"))
    .sort();

  const warnings = [];

  for (const migration of migrations) {
    const content = fs.readFileSync(
      path.join(migrationsDir, migration),
      "utf8",
    );
    for (const pattern of patterns) {
      if (pattern.test(content)) {
        warnings.push(
          `${migration} contains potentially dangerous operation: ${pattern}`,
        );
      }
    }
  }

  if (warnings.length > 0) {
    console.warn("⚠️  Database migration warnings:");
    warnings.forEach((warning) => console.warn(`   ${warning}`));
    console.warn("   Ensure proper rollback scripts exist");
  } else {
    console.log("✅ Database migrations safety check passed");
  }
}

async function checkSloCompliance({
  prometheusUrl = DEFAULT_PROMETHEUS_URL,
} = {}) {
  console.log("🔍 Checking SLO compliance");
  const fetchFn = await ensureFetch();

  for (const [metric, query] of Object.entries(PROMETHEUS_QUERIES)) {
    const response = await fetchFn(
      `${prometheusUrl}/api/v1/query?query=${encodeURIComponent(query)}`,
    );

    if (!response.ok) {
      throw new Error(
        `Prometheus query failed for ${metric}: ${response.statusText}`,
      );
    }

    const data = await response.json();

    if (!Array.isArray(data.data?.result) || data.data.result.length === 0) {
      console.warn(`⚠️  No Prometheus data for ${metric}`);
      continue;
    }

    const value = parseFloat(data.data.result[0].value[1]);
    const threshold = PROMETHEUS_SLOS[metric];

    if (Number.isNaN(value)) {
      console.warn(`⚠️  Could not parse value for ${metric}`);
      continue;
    }

    if (metric === "availability") {
      assert.ok(
        value >= threshold,
        `${metric} is ${value.toFixed(2)}%, below SLO of ${threshold}%`,
      );
    } else if (metric === "error_rate") {
      assert.ok(
        value <= threshold,
        `${metric} is ${value.toFixed(2)}%, above SLO of ${threshold}%`,
      );
    } else if (metric === "latency_p95") {
      assert.ok(
        value <= threshold,
        `${metric} is ${(value * 1000).toFixed(0)}ms, above SLO of ${(threshold * 1000).toFixed(0)}ms`,
      );
    }

    console.log(`✅ ${metric}: ${value.toFixed(2)} (SLO: ${threshold})`);
  }

  console.log("✅ SLO compliance check completed");
}

async function checkSecurityHeaders({ appUrl = DEFAULT_APP_URL } = {}) {
  console.log("🔍 Checking security headers");
  const fetchFn = await ensureFetch();

  const response = await fetchFn(appUrl);
  if (!response.ok) {
    throw new Error(
      `Failed to fetch ${appUrl}: ${response.status} ${response.statusText}`,
    );
  }

  const headers = response.headers;
  const requiredHeaders = {
    "strict-transport-security": /max-age=\d+/i,
    "x-content-type-options": /^nosniff$/i,
    "x-frame-options": /^(DENY|SAMEORIGIN)$/i,
    "x-xss-protection": /^1; mode=block$/i,
    "content-security-policy": /.+/,
  };

  for (const [header, expected] of Object.entries(requiredHeaders)) {
    const value = headers.get(header);
    assert.ok(value, `Missing security header: ${header}`);

    if (expected instanceof RegExp) {
      assert.ok(
        expected.test(value),
        `Header ${header} has unexpected value: ${value}`,
      );
    } else {
      assert.strictEqual(
        value,
        expected,
        `Header ${header} has incorrect value: ${value}`,
      );
    }

    console.log(`✅ ${header}: ${value}`);
  }

  console.log("✅ Security headers check passed");
}

async function run() {
  await checkCoupling();
  checkPerformanceBudgets();
  await checkApiStability();
  checkMigrations();
  await checkSloCompliance();
  await checkSecurityHeaders();
}

run()
  .then(() => {
    console.log("✅ All fitness functions completed");
  })
  .catch((err) => {
    console.error("❌ Fitness functions failed:", err.message);
    process.exit(1);
  });
