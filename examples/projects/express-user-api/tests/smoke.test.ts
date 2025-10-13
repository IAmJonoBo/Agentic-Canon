import { describe, it, expect } from "vitest";
import app from "../src/app.js";

describe("Express User API - Smoke Tests", () => {
  it("should export app", () => {
    expect(app).toBeDefined();
  });

  it("should have routes defined", () => {
    // Express app should have a router
    expect(app._router).toBeDefined();
  });
});
