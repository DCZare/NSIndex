using extension edgeql_http;

module default {
  type Work {
    optional pmid: float64;
    required journal: str;
    required doi: str;
    optional title: str;
    optional abstract: str;
    multi authors: Author;
    optional url: str;
    optional cited_by_accounts_count: str;
    optional cited_by_posts_count: str;
    optional cited_by_tweeters_count: str;
    optional cited_by_patents_count: str;
    optional cited_by_fbwalls_count: str;
    optional year: str;
    optional author_position: str;
    optional institution_name: str;


  }

  type Author {
    required name: str;
    multi works := (SELECT Work FILTER Work.authors = Author);
  }
}
