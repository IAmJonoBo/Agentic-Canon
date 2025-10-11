/**
 * Main entry point for {{cookiecutter.project_name}}
 */

export function ping(): string {
  return "pong";
}

export function greet(name: string): string {
  return `Hello, ${name}!`;
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  console.log("{{cookiecutter.project_name}} is running!");
  console.log(ping());
  console.log(greet("World"));
}
