const { initializeApp } = require('firebase-admin/app');
const { getStorage } = require('firebase-admin/storage');
initializeApp({ projectId: "hcdp-digital-inbox" });
getStorage().getBuckets().then(res => console.log("BUCKETS:", res[0].map(b => b.name))).catch(console.error);
