/**
 * Main entry point for Express User API
 */

import app from "./app.js";
import { logger } from "./logger.js";

const PORT = process.env.PORT || 3000;

// Start server
app.listen(PORT, () => {
  logger.info(`Express User API running on port ${PORT}`);
});

export { app };
export default app;
