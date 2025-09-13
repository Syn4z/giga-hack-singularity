const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());

// RESTful API routes
app.get('/api/tarriff', (req, res) => {
  res.json(tarriffs);
});

app.get('/api/consumption', (req, res) => {
  res.json(consumption);
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
