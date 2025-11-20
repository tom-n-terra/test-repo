
function simpleLogger(req, res, next) {
  const now = new Date().toISOString();
  console.log(`[${now}] ${req.method} ${req.originalUrl}`);

  // Continue to the next middleware/route handler
  next();
}

module.exports = simpleLogger;
