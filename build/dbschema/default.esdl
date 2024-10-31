module default {
  type Work {
    optional pmid: float64;
    required journal: str;
    required doi: str;
    optional title: str;
    optional work_publication_date: str;
    optional abstract: str;
    optional work_title: str;
    optional work_display_name: str;
    optional work_publication_year: str;
    optional author_position: str;
    optional institution_name: str;
    optional institution_id: str;
    optional institution_country_code: str;
    optional work_id: str;
    optional cited_by_accounts_count: str;
    optional cited_by_posts_count: str;
    optional cited_by_tweeters_count: str;
    optional cited_by_patents_count: str;
    multi authors: Author;
    optional url: str;
  }

  type Author {
    required name: str;
    multi works := (SELECT Work FILTER Work.authors = Author);
    optional First: str;
    optional Last: str;
    optional Lifespan: str;
    optional Gender: str;
    optional Ethnicity: str;
    optional Graduation_Year: str;
    optional Residency: str;
    optional Chair_Chief: str;
    optional Program_Director: str;
    optional Positions_Held: str;
  }
}
