'use client';

import { useEffect } from 'react';

export default function Home() {
  useEffect(() => {
    console.log("Home page rendered!");
  }, []);

  return (
    <main>
      <h1>Hello, world!</h1>
    </main>
  );
}
