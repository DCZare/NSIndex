'use client';
import { useState, useEffect } from "react";
import Link from 'next/link';
import Search from "@/components/Search";

type Work = {
  id: string;
  title: string;
  doi: string;
};

type Author = {
  id: string;
  name: string;
};

type SearchResult = Work | Author; // Combined type for works and authors

export default function Home() {
  const [searchValue, setSearchValue] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchSearchResults = async (searchValue: string) => {
    try {
      setLoading(true);
      const response = await fetch(`/api/searchWorks?q=${encodeURIComponent(searchValue)}`);
      const results = await response.json();
      setSearchResults(results);
    } catch (error) {
      console.error("Error fetching search results:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (value: string) => {
    setSearchValue(value);
  };

  useEffect(() => {
    if (searchValue.trim() !== '') {
      fetchSearchResults(searchValue);
    } else {
      setSearchResults([]);
    }
  }, [searchValue]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 w-full max-w-md items-center justify-between font-mono text-sm lg:flex-inline">
        <h1 className={'text-5xl my-10'}>UBNS Bibliometrics Search</h1>
        <Search onSearch={handleSearch} />
        <h2 className={'text-2xl mt-20 mx-2 underline'}>Searched for:</h2>
        <p className={'text-2xl m-2'}>{searchValue}</p>

        {loading ? (
          <p className="text-2xl m-2">Loading...</p>
        ) : searchResults.length > 0 ? (
          <div>
            {searchResults.map((result) => (
              <div key={result.id} className="my-4 p-4 border border-gray-300">
                <Link href={'doi' in result ? `/works/${result.id}` : `/author/${result.id}`}>
                  <h3 className="text-xl text-blue-600 underline cursor-pointer hover:text-blue-800">
                    {'title' in result ? (result as Work).title : (result as Author).name}
                  </h3>
                </Link>
                {'doi' in result && (
                  <p className="text-sm text-gray-500">{(result as Work).doi}</p>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p className="text-2xl m-2">No results found.</p>
        )}
      </div>
    </main>
  );
}
