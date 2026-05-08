const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
const serverId = process.env.SERVER_ID || 'server-1';

// Middleware
app.use(express.json());

// Routes
app.get('/', (req, res) => {
    res.json({
        message: 'Welcome to the Sample Web Application',
        timestamp: new Date().toISOString(),
        server_id: serverId,
        status: 'running'
    });
});

app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        server_id: serverId,
        uptime: process.uptime()
    });
});

app.get('/api/users', (req, res) => {
    res.json({
        users: [
            { id: 1, name: 'John Doe', email: 'john@example.com' },
            { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
            { id: 3, name: 'Bob Johnson', email: 'bob@example.com' }
        ],
        server_id: serverId,
        timestamp: new Date().toISOString()
    });
});

app.listen(port, () => {
    console.log(`Sample app listening on port ${port}`);
    console.log(`Server ID: ${serverId}`);
});