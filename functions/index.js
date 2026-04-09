/**
 * Import function triggers from their respective submodules:
 *
 * const {onCall} = require("firebase-functions/v2/https");
 * const {onDocumentWritten} = require("firebase-functions/v2/firestore");
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */

const functions = require("firebase-functions");
const admin = require("firebase-admin");
const fetch = require("node-fetch");

admin.initializeApp();
const db = admin.firestore();

const USER_IDS = [
  "68292fccf55f9440c28c67e8",
];

function buildUrl(userId) {
  return `https://api2.warera.io/trpc/user.getUserLite?batch=1&input={"0":{"userId":"${userId}"}}`;
}

exports.trackUsers = functions.pubsub
  .schedule("every 12 hours")
  .onRun(async () => {

    for (const userId of USER_IDS) {
      try {
        const res = await fetch(buildUrl(userId));
        const json = await res.json();
        const data = json[0].result.data;

        const entry = {
          fecha: new Date().toISOString(),
          usuario: data.username,
          userId: userId,
          userDamages: data.rankings.userDamages.value,
          userWealth: data.rankings.userWealth.value
        };

        await db.collection("stats").add(entry);

        console.log("Guardado:", entry.usuario);
      } catch (err) {
        console.error(err);
      }
    }

    return null;
  });