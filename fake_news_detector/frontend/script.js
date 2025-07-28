// ✅ Analyze news and add to history (without clearing textarea)
async function analyzeNews() {
  const newsText = document.getElementById("newsInput").value.trim();
  if (!newsText) return;

  try {
    const response = await fetch("https://fake-news-backend-1-hgvj.onrender.com/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: newsText })
    });

    const data = await response.json();
    const prediction = data.prediction;
    const confidence = Math.round(data.confidence * 100);

    // ✅ Show result directly under Analyze button
    const resultDiv = document.getElementById("latestResult");
    resultDiv.innerHTML = `
      <p>🧠 <strong>Latest Prediction:</strong> ${prediction}</p>
      <p>🎯 <strong>Confidence:</strong> ${confidence}%</p>
      <hr />
    `;

    addToHistory(newsText, prediction, confidence);

    // ❌ Don't clear the textarea
    // document.getElementById("newsInput").value = "";

  } catch (error) {
    console.error("Error connecting to backend:", error);
    document.getElementById("latestResult").innerHTML = `
      <p>❌ <strong>Error:</strong> Unable to get prediction from server.</p>
      <hr />
    `;
  }
}
