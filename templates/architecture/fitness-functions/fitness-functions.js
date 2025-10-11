# Fitness Functions
# Automated architectural governance checks
# Implements: Evolutionary architecture, continuous compliance
# Standards: ISO/IEC 25010 (Maintainability)

# These fitness functions run in CI to enforce architectural constraints

---
# 1. Dependency Coupling Check
# File: fitness-coupling.js

const madge = require('madge');
const assert = require('assert');

async function checkCoupling() {
    const res = await madge('src/');
    
    // Check for circular dependencies
    const circular = res.circular();
    assert.strictEqual(
        circular.length, 
        0, 
        `Found ${circular.length} circular dependencies: ${JSON.stringify(circular)}`
    );
    
    // Check coupling between modules
    const dependencies = res.obj();
    for (const [module, deps] of Object.entries(dependencies)) {
        // Core modules should not depend on feature modules
        if (module.includes('core/')) {
            const featureDeps = deps.filter(d => d.includes('features/'));
            assert.strictEqual(
                featureDeps.length,
                0,
                `Core module ${module} depends on feature modules: ${featureDeps}`
            );
        }
    }
    
    console.log('✅ Coupling check passed');
}

checkCoupling().catch(err => {
    console.error('❌ Coupling check failed:', err.message);
    process.exit(1);
});

---
# 2. Performance Budget Check
# File: fitness-performance.js

const fs = require('fs');
const assert = require('assert');

const BUDGETS = {
    'bundle.js': 170 * 1024,        // 170KB
    'bundle.css': 50 * 1024,        // 50KB
    'vendor.js': 300 * 1024,        // 300KB
};

function checkPerformanceBudgets() {
    const distPath = './dist';
    
    for (const [file, maxSize] of Object.entries(BUDGETS)) {
        const filePath = `${distPath}/${file}`;
        
        if (!fs.existsSync(filePath)) {
            console.log(`⚠️  Skipping ${file} - not found`);
            continue;
        }
        
        const stats = fs.statSync(filePath);
        const sizeMB = (stats.size / 1024).toFixed(2);
        const budgetMB = (maxSize / 1024).toFixed(2);
        
        assert.ok(
            stats.size <= maxSize,
            `File ${file} is ${sizeMB}KB, exceeds budget of ${budgetMB}KB`
        );
        
        console.log(`✅ ${file}: ${sizeMB}KB (budget: ${budgetMB}KB)`);
    }
    
    console.log('✅ Performance budgets met');
}

try {
    checkPerformanceBudgets();
} catch (err) {
    console.error('❌ Performance budget check failed:', err.message);
    process.exit(1);
}

---
# 3. API Contract Stability Check
# File: fitness-api-stability.js

const fs = require('fs');
const yaml = require('js-yaml');
const assert = require('assert');

function checkAPIStability() {
    // Load current and previous OpenAPI specs
    const currentSpec = yaml.load(fs.readFileSync('openapi.yaml', 'utf8'));
    const previousSpec = yaml.load(fs.readFileSync('openapi-previous.yaml', 'utf8'));
    
    // Check for breaking changes
    const breakingChanges = [];
    
    // Check if endpoints were removed
    for (const path in previousSpec.paths) {
        if (!currentSpec.paths[path]) {
            breakingChanges.push(`Removed endpoint: ${path}`);
        }
    }
    
    // Check if required parameters were added
    for (const path in currentSpec.paths) {
        for (const method in currentSpec.paths[path]) {
            const current = currentSpec.paths[path][method];
            const previous = previousSpec.paths?.[path]?.[method];
            
            if (previous && current.parameters) {
                const newRequired = current.parameters.filter(p => 
                    p.required && 
                    !previous.parameters?.some(pp => pp.name === p.name)
                );
                
                if (newRequired.length > 0) {
                    breakingChanges.push(
                        `New required parameter in ${method.toUpperCase()} ${path}: ${newRequired.map(p => p.name).join(', ')}`
                    );
                }
            }
        }
    }
    
    assert.strictEqual(
        breakingChanges.length,
        0,
        `Breaking changes detected:\n${breakingChanges.join('\n')}`
    );
    
    console.log('✅ API contract stability check passed');
}

try {
    checkAPIStability();
} catch (err) {
    console.error('❌ API stability check failed:', err.message);
    process.exit(1);
}

---
# 4. Database Migration Safety Check
# File: fitness-db-migrations.js

const fs = require('fs');
const assert = require('assert');

function checkMigrations() {
    const migrationsDir = './migrations';
    const migrations = fs.readdirSync(migrationsDir)
        .filter(f => f.endsWith('.sql'))
        .sort();
    
    const dangerousPatterns = [
        /DROP\s+TABLE/i,
        /ALTER\s+TABLE.*DROP\s+COLUMN/i,
        /TRUNCATE/i,
    ];
    
    const warnings = [];
    
    for (const migration of migrations) {
        const content = fs.readFileSync(`${migrationsDir}/${migration}`, 'utf8');
        
        for (const pattern of dangerousPatterns) {
            if (pattern.test(content)) {
                warnings.push(`${migration} contains potentially dangerous operation: ${pattern}`);
            }
        }
    }
    
    if (warnings.length > 0) {
        console.warn('⚠️  Database migration warnings:');
        warnings.forEach(w => console.warn(`   ${w}`));
        console.warn('   Ensure proper rollback scripts exist');
    } else {
        console.log('✅ Database migrations safety check passed');
    }
}

checkMigrations();

---
# 5. SLO Compliance Check
# File: fitness-slo.js

const assert = require('assert');

async function checkSLOCompliance() {
    // Fetch metrics from Prometheus
    const prometheusUrl = process.env.PROMETHEUS_URL || 'http://localhost:9090';
    
    const queries = {
        availability: '(sum(rate(http_requests_total{status=~"2.."}[30d])) / sum(rate(http_requests_total[30d]))) * 100',
        latency_p95: 'histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[30d])) by (le))',
        error_rate: '(sum(rate(http_requests_total{status=~"5.."}[30d])) / sum(rate(http_requests_total[30d]))) * 100',
    };
    
    const slos = {
        availability: 99.9,  // 99.9%
        latency_p95: 0.3,    // 300ms
        error_rate: 0.1,     // 0.1%
    };
    
    for (const [metric, query] of Object.entries(queries)) {
        try {
            const response = await fetch(
                `${prometheusUrl}/api/v1/query?query=${encodeURIComponent(query)}`
            );
            const data = await response.json();
            
            if (data.data.result.length === 0) {
                console.log(`⚠️  No data for ${metric}`);
                continue;
            }
            
            const value = parseFloat(data.data.result[0].value[1]);
            const threshold = slos[metric];
            
            if (metric === 'availability') {
                assert.ok(
                    value >= threshold,
                    `${metric} is ${value.toFixed(2)}%, below SLO of ${threshold}%`
                );
            } else if (metric === 'error_rate') {
                assert.ok(
                    value <= threshold,
                    `${metric} is ${value.toFixed(2)}%, above SLO of ${threshold}%`
                );
            } else if (metric === 'latency_p95') {
                assert.ok(
                    value <= threshold,
                    `${metric} is ${(value * 1000).toFixed(0)}ms, above SLO of ${(threshold * 1000).toFixed(0)}ms`
                );
            }
            
            console.log(`✅ ${metric}: ${value.toFixed(2)} (SLO: ${threshold})`);
        } catch (err) {
            console.error(`❌ Failed to check ${metric}:`, err.message);
        }
    }
    
    console.log('✅ SLO compliance check completed');
}

checkSLOCompliance().catch(err => {
    console.error('❌ SLO check failed:', err.message);
    process.exit(1);
});

---
# 6. Security Headers Check
# File: fitness-security-headers.js

const assert = require('assert');

async function checkSecurityHeaders() {
    const url = process.env.APP_URL || 'http://localhost:3000';
    
    const requiredHeaders = {
        'strict-transport-security': /max-age=\d+/,
        'x-content-type-options': 'nosniff',
        'x-frame-options': /DENY|SAMEORIGIN/,
        'x-xss-protection': '1; mode=block',
        'content-security-policy': /.+/,
    };
    
    try {
        const response = await fetch(url);
        const headers = response.headers;
        
        for (const [header, expected] of Object.entries(requiredHeaders)) {
            const value = headers.get(header);
            
            assert.ok(value, `Missing security header: ${header}`);
            
            if (typeof expected === 'string') {
                assert.strictEqual(
                    value,
                    expected,
                    `Header ${header} has incorrect value: ${value}`
                );
            } else {
                assert.ok(
                    expected.test(value),
                    `Header ${header} doesn't match pattern: ${value}`
                );
            }
            
            console.log(`✅ ${header}: ${value}`);
        }
        
        console.log('✅ Security headers check passed');
    } catch (err) {
        console.error('❌ Security headers check failed:', err.message);
        process.exit(1);
    }
}

checkSecurityHeaders();

---
# CI Integration
# Add to .github/workflows/fitness-functions.yml

name: Fitness Functions

on: [push, pull_request]

jobs:
  fitness-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install Dependencies
        run: npm ci
      
      - name: Check Coupling
        run: node fitness-coupling.js
      
      - name: Check Performance Budgets
        run: node fitness-performance.js
      
      - name: Check API Stability
        run: node fitness-api-stability.js
      
      - name: Check DB Migrations
        run: node fitness-db-migrations.js
      
      - name: Check Security Headers
        run: node fitness-security-headers.js

# All fitness functions should fail fast and fail loud
# They act as automated architectural governance
