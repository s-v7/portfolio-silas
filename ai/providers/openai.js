export async function askOpenAI(message) {
  const resp = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      input: message,
    }),
  });

  const data = await resp.json();

  if (!resp.ok) {
    throw new Error(JSON.stringify(data));
  }

  const text =
    data.output_text ||
    data.output?.[0]?.content?.[0]?.text ||
    data.output?.[0]?.content?.[0]?.value ||
    JSON.stringify(data, null, 2);

  return text;
}
