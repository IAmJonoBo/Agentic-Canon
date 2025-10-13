import { describe, it, expect } from "vitest";
import request from "supertest";
import app from "../src/app.js";

describe("Express User API", () => {
  describe("Health Endpoints", () => {
    it("should return healthy status from root", async () => {
      const response = await request(app).get("/");
      expect(response.status).toBe(200);
      expect(response.body.status).toBe("healthy");
      expect(response.body.service).toBe("Express User API");
    });

    it("should return healthy from /health", async () => {
      const response = await request(app).get("/health");
      expect(response.status).toBe(200);
      expect(response.body.status).toBe("healthy");
    });

    it("should return ready from /ready", async () => {
      const response = await request(app).get("/ready");
      expect(response.status).toBe(200);
      expect(response.body.status).toBe("ready");
    });
  });

  describe("User Management", () => {
    it("should create a new user", async () => {
      const userData = {
        email: "test@example.com",
        fullName: "Test User",
        password: "securepass123",
        role: "user",
      };

      const response = await request(app).post("/users").send(userData);

      expect(response.status).toBe(201);
      expect(response.body.email).toBe(userData.email);
      expect(response.body.fullName).toBe(userData.fullName);
      expect(response.body.id).toBeDefined();
      expect(response.body.password).toBeUndefined();
      expect(response.body.hashedPassword).toBeUndefined();
    });

    it("should not create user with duplicate email", async () => {
      const userData = {
        email: "duplicate@example.com",
        fullName: "Test User",
        password: "securepass123",
      };

      // Create first user
      await request(app).post("/users").send(userData);

      // Try to create duplicate
      const response = await request(app).post("/users").send(userData);

      expect(response.status).toBe(400);
      expect(response.body.error).toContain("already exists");
    });

    it("should validate user input", async () => {
      const invalidData = {
        email: "not-an-email",
        fullName: "",
        password: "short",
      };

      const response = await request(app).post("/users").send(invalidData);

      expect(response.status).toBe(400);
      expect(response.body.error).toBe("Validation error");
    });

    it("should list all users", async () => {
      const response = await request(app).get("/users");

      expect(response.status).toBe(200);
      expect(Array.isArray(response.body)).toBe(true);
    });

    it("should get user by ID", async () => {
      // Create user first
      const createResponse = await request(app).post("/users").send({
        email: "gettest@example.com",
        fullName: "Get Test",
        password: "securepass123",
      });

      const userId = createResponse.body.id;

      // Get the user
      const response = await request(app).get(`/users/${userId}`);

      expect(response.status).toBe(200);
      expect(response.body.id).toBe(userId);
      expect(response.body.email).toBe("gettest@example.com");
    });

    it("should return 404 for non-existent user", async () => {
      const response = await request(app).get("/users/00000000-0000-0000-0000-000000000000");

      expect(response.status).toBe(404);
    });

    it("should update a user", async () => {
      // Create user first
      const createResponse = await request(app).post("/users").send({
        email: "updatetest@example.com",
        fullName: "Update Test",
        password: "securepass123",
      });

      const userId = createResponse.body.id;

      // Update the user
      const response = await request(app)
        .put(`/users/${userId}`)
        .send({ fullName: "Updated Name" });

      expect(response.status).toBe(200);
      expect(response.body.fullName).toBe("Updated Name");
      expect(response.body.email).toBe("updatetest@example.com");
    });

    it("should delete a user", async () => {
      // Create user first
      const createResponse = await request(app).post("/users").send({
        email: "deletetest@example.com",
        fullName: "Delete Test",
        password: "securepass123",
      });

      const userId = createResponse.body.id;

      // Delete the user
      const deleteResponse = await request(app).delete(`/users/${userId}`);

      expect(deleteResponse.status).toBe(204);

      // Verify user is deleted
      const getResponse = await request(app).get(`/users/${userId}`);
      expect(getResponse.status).toBe(404);
    });
  });

  describe("Error Handling", () => {
    it("should return 404 for unknown routes", async () => {
      const response = await request(app).get("/unknown-route");

      expect(response.status).toBe(404);
      expect(response.body.error).toBe("Not found");
    });
  });
});
