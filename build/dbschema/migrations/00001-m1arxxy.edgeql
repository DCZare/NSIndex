CREATE MIGRATION m1arxxynkdyaeqj4vcjmc7lv5ey5atn4pozjsztayjr4zlhr5pwnsa
    ONTO initial
{
  CREATE EXTENSION edgeql_http VERSION '1.0';
  CREATE TYPE default::Author {
      CREATE REQUIRED PROPERTY name: std::str;
  };
  CREATE TYPE default::Work {
      CREATE MULTI LINK authors: default::Author;
      CREATE OPTIONAL PROPERTY abstract: std::str;
      CREATE OPTIONAL PROPERTY author_position: std::str;
      CREATE OPTIONAL PROPERTY cited_by_accounts_count: std::str;
      CREATE OPTIONAL PROPERTY cited_by_fbwalls_count: std::str;
      CREATE OPTIONAL PROPERTY cited_by_patents_count: std::str;
      CREATE OPTIONAL PROPERTY cited_by_posts_count: std::str;
      CREATE OPTIONAL PROPERTY cited_by_tweeters_count: std::str;
      CREATE REQUIRED PROPERTY doi: std::str;
      CREATE OPTIONAL PROPERTY institution_name: std::str;
      CREATE REQUIRED PROPERTY journal: std::str;
      CREATE OPTIONAL PROPERTY pmid: std::float64;
      CREATE OPTIONAL PROPERTY title: std::str;
      CREATE OPTIONAL PROPERTY url: std::str;
      CREATE OPTIONAL PROPERTY year: std::str;
  };
  ALTER TYPE default::Author {
      CREATE MULTI LINK works := (SELECT
          default::Work
      FILTER
          (default::Work.authors = default::Author)
      );
  };
};
