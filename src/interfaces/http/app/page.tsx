async function getCalculations() {
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL ?? 'http://localhost:3000';
  const response = await fetch(`${baseUrl}/api/calculations`, { cache: 'no-store' });

  if (!response.ok) {
    return [] as Array<{
      id: string;
      leftOperand: number;
      rightOperand: number;
      operation: string;
      result: number;
      createdAt: string;
    }>;
  }

  const payload = (await response.json()) as {
    data: Array<{
      id: string;
      leftOperand: number;
      rightOperand: number;
      operation: string;
      result: number;
      createdAt: string;
    }>;
  };

  return payload.data;
}

export default async function HomePage() {
  const calculations = await getCalculations();

  return (
    <main style={{ fontFamily: 'sans-serif', padding: '2rem', maxWidth: '960px', margin: '0 auto' }}>
      <h1>calculator migration full workflow test</h1>
      <p>Minimal Next.js interface backed by clean architecture use cases.</p>
      <section>
        <h2>Available API</h2>
        <p>
          POST <code>/api/calculations</code> with JSON:
        </p>
        <pre>{JSON.stringify({ leftOperand: 4, rightOperand: 2, operation: 'divide' }, null, 2)}</pre>
      </section>
      <section>
        <h2>Stored calculations</h2>
        {calculations.length === 0 ? (
          <p>No calculations yet. Create one through the API.</p>
        ) : (
          <ul>
            {calculations.map((calculation) => (
              <li key={calculation.id}>
                {calculation.leftOperand} {calculation.operation} {calculation.rightOperand} = {calculation.result}
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
