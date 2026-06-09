const { initializeApp, cert } = require('firebase-admin/app');
const { getStorage } = require('firebase-admin/storage');

initializeApp({
  // Use default credentials since we are logged into gcloud/firebase
  projectId: "hcdp-digital-inbox"
});

async function setCors() {
  const bucket = getStorage().bucket("hcdp-digital-inbox.firebasestorage.app");
  await bucket.setCorsConfiguration([
    {
      origin: ["*"],
      method: ["GET", "PUT", "POST", "DELETE", "OPTIONS"],
      maxAgeSeconds: 3600
    }
  ]);
  console.log("CORS set successfully!");
}

setCors().catch(console.error);
