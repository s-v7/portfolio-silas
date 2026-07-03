export async function askNvidia(message) {
  const resp = await fetch("https://integrate.api.nvidia.com/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.NVIDIA_API_KEY}`,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({
      model: "meta/llama-3.1-70b-instruct",
      messages: [{ role: "user", content: message }],
      temperature: 0.2,
      max_tokens: 800,
    }),
  });

  const raw = await resp.text();

  if (!resp.ok) {
    throw new Error(raw);
  }

  const data = JSON.parse(raw);
  return data.choices?.[0]?.message?.content || raw;
}
