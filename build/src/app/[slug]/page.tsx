type PageProps = {
  params: Promise<{
    slug: string;
  }>;
};

export default async function DynamicPage({ params }: PageProps) {
  const { slug } = await params; // Awaiting the params to handle the Promise type

  return (
    <main className="flex min-h-screen items-center justify-center">
      <h1 className="text-5xl">{slug}</h1>
    </main>
  );
}
