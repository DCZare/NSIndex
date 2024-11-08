export default async function DynamicPage({ params }: { params: { slug: string } }) {
  // Simulating async behavior by ensuring `params` is accessed asynchronously
  const slug = await Promise.resolve(params.slug);

  return (
    <main className="flex min-h-screen items-center justify-center">
      <h1 className="text-5xl">{slug}</h1>
    </main>
  );
}
