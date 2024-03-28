const { PubSub } = require('@google-cloud/pubsub');
const express = require('express');
const app = express();

const projectId = 'elated-nectar-413615';
const subscriptionName = 'TestTopic-sub';
const pubsub = new PubSub({ projectId });

// Subscribe to a Pub/Sub topic
const subscription = pubsub.subscription(subscriptionName);

// Listen for new messages
subscription.on('message', messageHandler);

function messageHandler(message) {
  console.log(`Received message: ${message.data}`);
  // Here, you can emit this message to the client-side
  // using WebSocket, Socket.io, or any other method of your choice
  // For simplicity, I'll just log it here.
  message.ack();
}

// Serve your HTML page
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
