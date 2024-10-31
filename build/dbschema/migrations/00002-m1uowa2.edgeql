CREATE MIGRATION m1uowa2lrea2lg3lpu4fzyxgst56uwbc7fmfok5zhhgbozqfaxrizq
    ONTO m1arxxynkdyaeqj4vcjmc7lv5ey5atn4pozjsztayjr4zlhr5pwnsa
{
  ALTER TYPE default::Author {
      CREATE OPTIONAL PROPERTY Chair_Chief: std::str;
      CREATE OPTIONAL PROPERTY Ethnicity: std::str;
      CREATE OPTIONAL PROPERTY First: std::str;
      CREATE OPTIONAL PROPERTY Gender: std::str;
      CREATE OPTIONAL PROPERTY Graduation_Year: std::str;
      CREATE OPTIONAL PROPERTY Last: std::str;
      CREATE OPTIONAL PROPERTY Lifespan: std::str;
      CREATE OPTIONAL PROPERTY Positions_Held: std::str;
      CREATE OPTIONAL PROPERTY Program_Director: std::str;
      CREATE OPTIONAL PROPERTY Residency: std::str;
  };
  ALTER TYPE default::Work {
      ALTER PROPERTY cited_by_fbwalls_count {
          RENAME TO institution_country_code;
      };
  };
  ALTER TYPE default::Work {
      CREATE OPTIONAL PROPERTY work_display_name: std::str;
  };
  ALTER TYPE default::Work {
      CREATE OPTIONAL PROPERTY work_id: std::str;
  };
  ALTER TYPE default::Work {
      CREATE OPTIONAL PROPERTY work_publication_date: std::str;
  };
  ALTER TYPE default::Work {
      CREATE OPTIONAL PROPERTY work_publication_year: std::str;
  };
  ALTER TYPE default::Work {
      CREATE OPTIONAL PROPERTY work_title: std::str;
  };
  ALTER TYPE default::Work {
      ALTER PROPERTY year {
          RENAME TO institution_id;
      };
  };
  DROP EXTENSION edgeql_http;
};
