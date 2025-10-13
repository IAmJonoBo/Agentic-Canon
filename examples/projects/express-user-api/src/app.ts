import express, { Request, Response, NextFunction } from "express";
import helmet from "helmet";
import cors from "cors";
import { ZodError } from "zod";
import { db } from "./database.js";
import { logger } from "./logger.js";
import { createUserSchema, updateUserSchema } from "./types.js";

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Request logging middleware
app.use((req: Request, res: Response, next: NextFunction) => {
  logger.info(`${req.method} ${req.path}`);
  next();
});

/**
 * Health check endpoints
 */
app.get("/", (req: Request, res: Response) => {
  res.json({
    status: "healthy",
    service: "Express User API",
    version: "0.1.0",
    timestamp: new Date().toISOString(),
  });
});

app.get("/health", (req: Request, res: Response) => {
  res.json({ status: "healthy" });
});

app.get("/ready", (req: Request, res: Response) => {
  res.json({ status: "ready" });
});

/**
 * User Management Endpoints
 */

// Create user
app.post("/users", (req: Request, res: Response) => {
  try {
    const input = createUserSchema.parse(req.body);

    // Check if user already exists
    const existing = db.getByEmail(input.email);
    if (existing) {
      return res.status(400).json({ error: "User with this email already exists" });
    }

    // Hash password (simplified for demo - use bcrypt in production)
    const hashedPassword = `hashed_${input.password}`;

    const user = db.create(input, hashedPassword);
    logger.info("User created", { userId: user.id, email: user.email });

    res.status(201).json(user);
  } catch (error) {
    if (error instanceof ZodError) {
      return res.status(400).json({ error: "Validation error", details: error.errors });
    }
    logger.error("Error creating user", { error });
    res.status(500).json({ error: "Internal server error" });
  }
});

// List users
app.get("/users", (req: Request, res: Response) => {
  const users = db.list();
  res.json(users);
});

// Get user by ID
app.get("/users/:id", (req: Request, res: Response) => {
  const user = db.get(req.params.id);
  if (!user) {
    return res.status(404).json({ error: "User not found" });
  }
  res.json(user);
});

// Update user
app.put("/users/:id", (req: Request, res: Response) => {
  try {
    const input = updateUserSchema.parse(req.body);

    // Check if user exists
    const existing = db.get(req.params.id);
    if (!existing) {
      return res.status(404).json({ error: "User not found" });
    }

    // Check if email is being changed and already exists
    if (input.email && input.email !== existing.email) {
      const emailUser = db.getByEmail(input.email);
      if (emailUser) {
        return res.status(400).json({ error: "User with this email already exists" });
      }
    }

    const user = db.update(req.params.id, input);
    logger.info("User updated", { userId: req.params.id });

    res.json(user);
  } catch (error) {
    if (error instanceof ZodError) {
      return res.status(400).json({ error: "Validation error", details: error.errors });
    }
    logger.error("Error updating user", { error });
    res.status(500).json({ error: "Internal server error" });
  }
});

// Delete user
app.delete("/users/:id", (req: Request, res: Response) => {
  const success = db.delete(req.params.id);
  if (!success) {
    return res.status(404).json({ error: "User not found" });
  }
  logger.info("User deleted", { userId: req.params.id });
  res.status(204).send();
});

// Error handling middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  logger.error("Unhandled error", { error: err });
  res.status(500).json({ error: "Internal server error" });
});

// 404 handler
app.use((req: Request, res: Response) => {
  res.status(404).json({ error: "Not found" });
});

// Start server only if not in test mode
if (process.env.NODE_ENV !== "test") {
  app.listen(PORT, () => {
    logger.info(`Server running on port ${PORT}`);
  });
}

export default app;
