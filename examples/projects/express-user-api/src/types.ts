import { z } from "zod";

/**
 * User role enumeration
 */
export enum UserRole {
  ADMIN = "admin",
  USER = "user",
  GUEST = "guest",
}

/**
 * Zod schema for user creation
 */
export const createUserSchema = z.object({
  email: z.string().email("Invalid email format"),
  fullName: z.string().min(1, "Full name is required").max(100, "Full name too long"),
  password: z.string().min(8, "Password must be at least 8 characters"),
  role: z.nativeEnum(UserRole).default(UserRole.USER),
});

/**
 * Zod schema for user updates
 */
export const updateUserSchema = z.object({
  email: z.string().email().optional(),
  fullName: z.string().min(1).max(100).optional(),
  password: z.string().min(8).optional(),
  role: z.nativeEnum(UserRole).optional(),
  isActive: z.boolean().optional(),
});

/**
 * User type
 */
export interface User {
  id: string;
  email: string;
  fullName: string;
  role: UserRole;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

/**
 * User creation type
 */
export type CreateUserInput = z.infer<typeof createUserSchema>;

/**
 * User update type
 */
export type UpdateUserInput = z.infer<typeof updateUserSchema>;

/**
 * User stored in database (with hashed password)
 */
export interface UserInDB extends User {
  hashedPassword: string;
}
