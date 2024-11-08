type PageProps = {
  params: {
    slug: string;
  };
};

export default async function DynamicPage({ params }: PageProps) {
  const slug = params.slug; // This should be awaited or fetched if needed

  return (
    <main className="flex min-h-screen items-center justify-center">
      <h1 className="text-5xl">{slug}</h1>
    </main>
  );
}
