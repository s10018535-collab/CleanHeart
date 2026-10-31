/*
# Civic issue reporting: issues and officer access

1. New Tables
- `issues`: citizen reports with title, description, address, the department it was routed to, priority (normal or urgent), status (new, in_progress, resolved), a photo URL and a creation time.
- `officer_credentials`: one row holding a salted SHA-256 hash of the officer portal password. The browser can never read it.
- `officer_sessions`: short-lived login tokens issued after a successful officer login. Each token is tied to one department.

2. Security
- Row level security is enabled on all three tables.
- `issues`: anyone can read posts and create new ones, but only with status "new". There is no public update or delete.
- Officer tables have no policies and no grants for browser roles. Only the server-side officer function (service role) can use them.

3. Seed Data
- Six example posts are added once, only when the issues table is empty.

4. Important Notes
1. Status changes happen only through the officer function, which checks the officer token and the department before updating.
2. The officer password is stored only as a hash.
*/

CREATE TABLE IF NOT EXISTS issues (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL CHECK (char_length(title) BETWEEN 3 AND 120),
  description text NOT NULL CHECK (char_length(description) BETWEEN 10 AND 2000),
  address text NOT NULL CHECK (char_length(address) BETWEEN 5 AND 200),
  department text NOT NULL CHECK (department IN ('Public Works', 'Water & Drainage', 'Sanitation', 'Electrical & Lighting', 'Parks & Recreation', 'Public Safety', 'General Services')),
  priority text NOT NULL DEFAULT 'normal' CHECK (priority IN ('normal', 'urgent')),
  status text NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'in_progress', 'resolved')),
  photo_url text NOT NULL CHECK (photo_url LIKE 'https://%'),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS issues_department_created_idx ON issues (department, created_at DESC);

CREATE TABLE IF NOT EXISTS officer_credentials (
  id integer PRIMARY KEY DEFAULT 1 CHECK (id = 1),
  salt text NOT NULL,
  password_hash text NOT NULL
);

CREATE TABLE IF NOT EXISTS officer_sessions (
  token text PRIMARY KEY,
  department text NOT NULL,
  expires_at timestamptz NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE issues ENABLE ROW LEVEL SECURITY;
ALTER TABLE officer_credentials ENABLE ROW LEVEL SECURITY;
ALTER TABLE officer_sessions ENABLE ROW LEVEL SECURITY;

INSERT INTO officer_credentials (id, salt, password_hash)
VALUES (
  1,
  'cleanhearts-officer-v1',
  encode(sha256(convert_to('cleanhearts-officer-v1:Govt@123', 'UTF8')), 'hex')
)
ON CONFLICT (id) DO NOTHING;

GRANT SELECT, INSERT ON issues TO anon, authenticated;
GRANT SELECT, UPDATE (status) ON issues TO service_role;
GRANT SELECT ON officer_credentials TO service_role;
GRANT SELECT, INSERT, DELETE ON officer_sessions TO service_role;

DROP POLICY IF EXISTS "public_read_issues" ON issues;
CREATE POLICY "public_read_issues" ON issues FOR SELECT
  TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "public_insert_new_issues" ON issues;
CREATE POLICY "public_insert_new_issues" ON issues FOR INSERT
  TO anon, authenticated WITH CHECK (status = 'new');

INSERT INTO issues (title, description, address, department, priority, status, photo_url, created_at)
SELECT v.title, v.description, v.address, v.department, v.priority, v.status, v.photo_url, v.created_at
FROM (VALUES
  ('Deep pothole on Maple Avenue near the elementary school', 'A pothole about the size of a car tire has opened in the right lane. Cars are swerving into the bike lane to avoid it, and it gets worse after every rain.', '214 Maple Avenue, Riverside', 'Public Works', 'normal', 'in_progress', 'https://images.pexels.com/photos/6018646/pexels-photo-6018646.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', now() - interval '2 days'),
  ('Water main burst flooding the sidewalk', 'Water is bubbling up through the pavement and has flooded the sidewalk. Pedestrians are stepping into the road to get around it. Please send a crew as soon as possible.', 'Harbor Road, outside Baker Market', 'Water & Drainage', 'urgent', 'new', 'https://images.pexels.com/photos/28447789/pexels-photo-28447789.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', now() - interval '1 hour'),
  ('Streetlight out for three nights on Oak Lane', 'The streetlight outside number 12 has been dark since Monday. The corner is pitch black at night and feels unsafe for people walking home.', 'Oak Lane and 5th Street', 'Electrical & Lighting', 'normal', 'new', 'https://images.pexels.com/photos/9971141/pexels-photo-9971141.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', now() - interval '5 hours'),
  ('Overflowing bins behind the market', 'Three bins have been overflowing for a week. Rubbish is spilling onto the lane and attracting rats. The area smells terrible in the afternoon heat.', '18 Market Lane, Eastside', 'Sanitation', 'normal', 'resolved', 'https://images.pexels.com/photos/4651148/pexels-photo-4651148.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', now() - interval '4 days'),
  ('Broken swing and rusted slide at Willow Park', 'One of the swings has snapped its chain and the slide has rusted through near the bottom. Several families have stopped bringing their children here.', 'Willow Park, north playground', 'Parks & Recreation', 'normal', 'new', 'https://images.pexels.com/photos/32801503/pexels-photo-32801503.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', now() - interval '1 day'),
  ('Crosswalk signal never gives pedestrians a walk sign', 'Pedestrians wait several minutes and the walk signal never appears. Children crossing to school are taking a real risk. This is a safety hazard.', 'Pine Street and Central Avenue', 'Public Safety', 'urgent', 'in_progress', 'https://images.pexels.com/photos/10121600/pexels-photo-10121600.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', now() - interval '3 hours')
) AS v(title, description, address, department, priority, status, photo_url, created_at)
WHERE NOT EXISTS (SELECT 1 FROM issues);
