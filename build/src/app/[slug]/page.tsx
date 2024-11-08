import { use } from 'react';

type PageProps = {
  params: {
    slug: string;
  };
};

export async function generateStaticParams() {
  // Return an empty array if you don't need static generation
  return [];
}

export default function DynamicPage({ params }: PageProps) {
  // Ensure `params` is accessed synchronously in the client component
  const slug = use(() => params.slug); // Ensure params is accessed correctly

  return (
    <main className="flex min-h-screen items-center justify-center">
      <h1 className="text-5xl">{slug}</h1>
    </main>
  );
}
