-- Drop tables if they exist
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS stories;
DROP TABLE IF EXISTS users;

-- Create Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    profile_picture_url TEXT  -- Add this line for avatar URL
);

-- Create Stories Table
CREATE TABLE stories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    likes INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create Comments Table
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    story_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    likes INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (story_id) REFERENCES stories (id)
);



-- Insert Sample Users with Avatars
INSERT INTO users (username, email, hash, profile_picture_url) VALUES
('user1', 'user1@example.com', 'hashed_password1', 'avatar1.png'),
('user2', 'user2@example.com', 'hashed_password2', 'avatar2.png'),
('user3', 'user3@example.com', 'hashed_password3', 'avatar3.png'),
('user4', 'user4@example.com', 'hashed_password4', 'avatar4.png'),
('user5', 'user5@example.com', 'hashed_password5', 'avatar5.png'),
('user6', 'user6@example.com', 'hashed_password6', 'avatar6.png'),
('user7', 'user7@example.com', 'hashed_password7', 'avatar7.png'),
('user8', 'user8@example.com', 'hashed_password8', 'avatar8.png'),
('user9', 'user9@example.com', 'hashed_password9', 'avatar9.png'),
('user10', 'user10@example.com', 'hashed_password10', 'avatar10.png');

-- Insert Sample Stories
INSERT INTO stories (user_id, title, text) VALUES 
(1, 'A dark time in my life', 'I felt completely lost and overwhelmed. Every day was a struggle, and I didn’t see any light at the end of the tunnel. I often thought about giving up, but I knew I had to keep going for my family.'),
(2, 'Thoughts of ending it all', 'I’ve been in a dark place for so long that I can’t remember what happiness feels like. There were days when I thought about ending it all, feeling like I was a burden to everyone around me.'),
(3, 'The weight of despair', 'Living with depression is like carrying a heavy weight that never goes away. I try to smile and pretend everything is fine, but inside I am screaming for help.'),
(4, 'Hope in the darkness', 'Despite everything, I found a glimmer of hope. I began talking to a therapist and found that sharing my thoughts alleviated some of the burden. It’s a long journey, but I’m learning to take it one day at a time.'),
(5, 'Finding strength', 'I didn’t think I had any strength left, but I discovered that sharing my story helped others as well. Together, we are fighting our battles, and it gives me the courage to face each day.'),
(6, 'Life feels unbearable', 'I often wonder if life is worth living. Some days, the pain feels like too much to bear. But then I see a kind word from a friend or a stranger, and it reminds me that there’s still beauty in the world.'),
(7, 'Fighting the demons', 'Every night, I fight the demons in my mind that tell me I am worthless. I’ve learned that I am not alone in this battle, and there are people who care about me.'),
(8, 'The struggle to stay alive', 'When the thoughts of suicide creep in, I remind myself of the people who love me. I try to hold on to the moments of joy, however small they may be.'),
(9, 'A glimpse of hope', 'During my darkest times, I found solace in the stories of others who have struggled. Their journeys inspired me to seek help and keep pushing forward.'),
(10, 'Turning pain into purpose', 'My experiences have led me to advocate for mental health awareness. Sharing my story has become my purpose, and I hope to help others who are in pain.'),
(11, 'Living with anxiety', 'Anxiety consumes me daily, but I am learning to manage it one breath at a time. It’s a constant battle, but I refuse to let it control my life.'),
(12, 'The loss of a loved one', 'Losing someone I loved deeply shattered my world. I often find myself spiraling into grief, but I know they would want me to keep living.'),
(13, 'Breaking the cycle', 'I grew up in a toxic environment, and it took years for me to break free. It’s still a struggle, but I am committed to my healing process.'),
(14, 'Hope after despair', 'I hit rock bottom last year, but I discovered that there’s hope even in the darkest moments. Reaching out to others has saved me.'),
(15, 'The fight for normalcy', 'Every day feels like a fight. I strive for a sense of normalcy, but it often feels out of reach. I hold on to small victories.'),
(16, 'Finding light in dark places', 'I learned to find light in the darkest places. Even on my worst days, I try to find one thing to be grateful for.'),
(17, 'Struggling with self-worth', 'I often struggle with feelings of unworthiness. I’m learning that I am enough, just as I am.'),
(18, 'Overcoming fear', 'Fear has held me back for so long. I’m starting to take small steps to confront it head-on.'),
(19, 'The journey of healing', 'Healing is not linear. There are ups and downs, but I keep pushing forward. I remind myself that progress is progress.'),
(20, 'Creating a support network', 'I reached out to others and created a support network. It has made all the difference in my healing journey.'),
(21, 'The silence of depression', 'Sometimes, the silence of depression is the loudest. I’ve learned to break that silence by speaking out.'),
(22, 'A message to others', 'If you are struggling, please know that it’s okay to ask for help. You are not alone in this fight.'),
(23, 'Rediscovering joy', 'I’m slowly rediscovering joy in life’s little moments. It’s a beautiful journey, even with its challenges.'),
(24, 'Support from friends', 'My friends have been my lifeline. Their support has helped me navigate through the darkest times.'),
(25, 'From pain to passion', 'I turned my pain into passion by writing. It has been a therapeutic outlet for me.'),
(26, 'Embracing vulnerability', 'I’ve learned that being vulnerable is a strength, not a weakness. It connects us to others.'),
(27, 'Life after trauma', 'Life after trauma is challenging, but I’m determined to rebuild. Each day is a new opportunity.'),
(28, 'Finding my voice', 'I finally found my voice after years of silence. I will not be silenced again.'),
(29, 'The power of stories', 'Sharing stories has the power to heal. I hope my story resonates with someone.'),
(30, 'A journey to self-acceptance', 'Accepting myself has been the hardest journey, but it’s also the most rewarding. I’m learning to love who I am.');

-- Insert Sample Comments
INSERT INTO comments (user_id, story_id, text) VALUES
(1, 1, 'Thank you for sharing your story. It resonates with me.'),
(2, 2, 'I understand what you are going through. You are not alone.'),
(3, 1, 'Your strength is inspiring. Keep fighting!'),
(4, 3, 'I have felt the same way. Let’s talk.'),
(5, 4, 'Hope is a powerful thing. Thank you for this.'),
(6, 5, 'Your words are powerful. I admire your courage.'),
(7, 6, 'You are not alone in this fight. Keep going.'),
(8, 7, 'Thank you for your honesty. It helps others feel less isolated.'),
(9, 8, 'Every day is a new chance. I believe in you.'),
(10, 9, 'Your story touched my heart. Thank you for sharing.'),
(11, 10, 'You’re turning your pain into purpose. That’s amazing.'),
(12, 1, 'It’s important to keep fighting. You’re stronger than you think.'),
(13, 2, 'I can relate to your struggle. You are brave for sharing.'),
(14, 3, 'Your journey is inspiring. Thank you for opening up.'),
(15, 4, 'You have a voice that matters. Keep sharing your story.'),
(16, 5, 'This gives me hope. Thank you for being vulnerable.'),
(17, 6, 'Your resilience is admirable. Keep pushing forward.'),
(18, 7, 'You are not alone. We are all in this together.'),
(19, 8, 'Every little step counts. You are doing great.'),
(20, 9, 'Thank you for being a light in the darkness.'),
(21, 10, 'Your advocacy for mental health is so important.'),
(22, 11, 'Thank you for sharing your journey with us.'),
(23, 12, 'Your courage to speak out is inspiring.'),
(24, 13, 'I’ve been through similar experiences. Thank you for sharing.'),
(25, 14, 'You are a warrior. Your story will inspire many.'),
(26, 15, 'Life is a journey. Thank you for reminding us of that.'),
(27, 16, 'You are deserving of happiness. Keep fighting for it.'),
(28, 17, 'Your story will resonate with others. Thank you.'),
(29, 18, 'It takes strength to face fears. Keep going!'),
(30, 19, 'You are making progress, and that’s what matters.');

-- Additional Comments for More Interaction
INSERT INTO comments (user_id, story_id, text) VALUES
(1, 20, 'Building a support network is so crucial. Great job!'),
(2, 21, 'Breaking the silence can be powerful. Thank you for sharing.'),
(3, 22, 'You are a beacon of hope for others. Keep shining!'),
(4, 23, 'Rediscovering joy is a beautiful journey. I’m with you!'),
(5, 24, 'Friends are such a blessing in difficult times.'),
(6, 25, 'Your passion is inspiring. Keep using your voice!'),
(7, 26, 'Vulnerability connects us all. Thank you for your strength.'),
(8, 27, 'Rebuilding after trauma is hard. I admire your courage.'),
(9, 28, 'Finding your voice is powerful. Keep it loud!'),
(10, 29, 'Stories indeed have the power to heal. Thank you!'),
(11, 30, 'Self-acceptance is key. You’re on the right path!'),
(12, 1, 'Your story is inspiring. Thank you for sharing it!'),
(13, 2, 'You are not alone in this battle. I am here for you!'),
(14, 3, 'Your words bring comfort. Keep writing and sharing!'),
(15, 4, 'It’s okay to ask for help. We are in this together.');
--for exc the script follow this
--sqlite3 hate.db
--.read scriptdemo.sql
