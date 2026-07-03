export async function askAnthropic(message) {
  const resp = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "x-api-key": process.env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "claude-3-5-haiku-latest",
      max_tokens: 1024,
      messages: [{ role: "user", content: message }],
    }),
  });

  const data = await resp.json();

  if (!resp.ok) {
    throw new Error(JSON.stringify(data));
  }

  return data.content?.[0]?.text || "No response";
}
