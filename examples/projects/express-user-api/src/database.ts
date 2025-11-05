import { randomUUID } from "crypto";
import { User, UserInDB, CreateUserInput, UpdateUserInput } from "./types.js";

/**
 * Simple in-memory database for demonstration
 */
class UserDatabase {
  private users: Map<string, UserInDB> = new Map();
  private emailIndex: Map<string, string> = new Map();

  /**
   * Create a new user
   */
  create(input: CreateUserInput, hashedPassword: string): User {
    const id = randomUUID();
    const now = new Date();

    const user: UserInDB = {
      id,
      email: input.email,
      fullName: input.fullName,
      role: input.role,
      isActive: true,
      hashedPassword,
      createdAt: now,
      updatedAt: now,
    };

    this.users.set(id, user);
    this.emailIndex.set(input.email, id);

    return this.toPublicUser(user);
  }

  /**
   * Get user by ID
   */
  get(id: string): User | undefined {
    const user = this.users.get(id);
    return user ? this.toPublicUser(user) : undefined;
  }

  /**
   * Get user by email
   */
  getByEmail(email: string): User | undefined {
    const id = this.emailIndex.get(email);
    if (!id) return undefined;
    const user = this.users.get(id);
    return user ? this.toPublicUser(user) : undefined;
  }

  /**
   * Get user with password by email (for authentication)
   */
  getByEmailWithPassword(email: string): UserInDB | undefined {
    const id = this.emailIndex.get(email);
    return id ? this.users.get(id) : undefined;
  }

  /**
   * Update a user
   */
  update(id: string, input: UpdateUserInput): User | undefined {
    const user = this.users.get(id);
    if (!user) return undefined;

    // Update email index if email changed
    if (input.email && input.email !== user.email) {
      this.emailIndex.delete(user.email);
      this.emailIndex.set(input.email, id);
    }

    const updated: UserInDB = {
      ...user,
      ...input,
      updatedAt: new Date(),
    };

    this.users.set(id, updated);
    return this.toPublicUser(updated);
  }

  /**
   * Delete a user
   */
  delete(id: string): boolean {
    const user = this.users.get(id);
    if (!user) return false;

    this.users.delete(id);
    this.emailIndex.delete(user.email);
    return true;
  }

  /**
   * List all users
   */
  list(): User[] {
    return Array.from(this.users.values()).map((user) => this.toPublicUser(user));
  }

  /**
   * Convert UserInDB to User (remove password)
   */
  private toPublicUser(user: UserInDB): User {
    const { hashedPassword, ...publicUser } = user;
    return publicUser;
  }
}

// Export singleton instance
export const db = new UserDatabase();
