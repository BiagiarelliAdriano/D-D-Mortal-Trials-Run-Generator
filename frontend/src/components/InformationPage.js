import React from "react";
import "../styles/InformationPage.css";

const informationPosts = [
    {
        icon: "fa-solid fa-scroll",
        title: "The Mortal Trials Guide",
        description:
            "Discover what The Mortal Trials is, how the game works, and everything you need to know to begin your journey through the Trials.",
        link: "https://docs.google.com/document/d/1qyfc7XC0qMIhDIjGb05Ognp-anXofgx8oHQPyCCAQoU/edit?usp=sharing",
        linkText: "Read the Guide"
    },
    {
        icon: "fa-solid fa-dungeon",
        title: "The Run Structure",
        description:
            "Learn how a Mortal Trials Run is structured, from the beginning of a Run through Encounters, progression, rewards, and everything in between.",
        link: "https://docs.google.com/document/d/1YDEq6jWRIzZ7bX608LMFlJd50i5jCqh2c46rZyEWNb8/edit?usp=sharing",
        linkText: "Explore the Run Structure"
    },
    {
        icon: "fa-solid fa-dragon",
        title: "Monsters & Items",
        description:
            "Browser the collection of monsters, items, and other gameplay content available throughout The Mortal Trials. Bolded text is either Homebrew content or adjusted content.",
        link: "https://docs.google.com/spreadsheets/d/1ViZiKNgPuFm4yQrq5Z0Ma79wO4dXq2hmO_H4lFeWerY/edit?usp=sharing",
        linkText: "Open the Database"
    },
    {
        icon: "fa-solid fa-bolt",
        title: "Environmental Wild Surges",
        description:
            "Learn about Environmental Wild Surges, their effects, and how these unpredictable forces can reshape the challenges faced during a Trial.",
        link: "https://docs.google.com/document/d/17URU9dMx-eK2o6rgwo-SpIZxGVSwkS0rs_znHRUIvM0/edit?usp=sharing",
        linkText: "Learn About Wild Surges"
    },
    {
        icon: "fa-solid fa-book-open",
        title: "Rules Compendium",
        description:
            "A reference for the rules, homebrew mechanics, adjusted content, clarifications, and special rulings used throughout The Mortal Trials.",
        link: "https://docs.google.com/spreadsheets/d/1seGtbDZQvejBgCj_FWb_HEkMEPTmeRtuESHiFeCMxXA/edit?usp=sharing",
        linkText: "Open the Compendium"
    },
    {
        icon: "fa-brands fa-discord",
        title: "The Mortal Trials Discord",
        description:
            "Join the community, discuss the Trials, find other players, share your experiences, and keep up with announcements and development with continues updates.",
        link: "https://discord.gg/CmNqX7Mrtp",
        linkText: "Join the Discord"
    },
    {
        icon: "fa-brands fa-patreon",
        title: "Support The Mortal Trials",
        description:
            "Support the continued development of The Mortal Trials through Patreon and help the project grow.",
        link: "https://patreon.com/TheMortalTrials?utm_medium=unknown&utm_source=join_link&utm_campaign=creatorshare_creator&utm_content=copyLink",
        linkText: "Visit Patreon"
    },
    {
        icon: "fa-brands fa-youtube",
        title: "The Mortal Trials on Youtube",
        description:
            "Watch The Mortal Trials content, demonstrations, development videos, updates, and more on the project's Youtube channle.",
        link: "https://www.youtube.com/@TheMortalTrials",
        linkText: "Visit Youtube"
    }
];

function InformationPage() {
    return (
        <div className="information-page">
            <header className="information-header">
                <div className="information-header-decoration">
                    ✦
                </div>
                <h1>The Mortal Trials</h1>
                <h2>Information & Resources</h2>
                <p>
                    Everything you need to understand, explore, and join
                    The Mortal Trials.
                </p>
            </header>
            <main className="information-content">
                <div className="information-grid">
                    {informationPosts.map((post, index) => (
                        <a
                            key={index}
                            href={post.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="information-card"
                        >
                            <div className="information-card-icon">
                                <i className={post.icon}></i>
                            </div>
                            <div className="information-card-content">
                                <h3>{post.title}</h3>
                                <p>{post.description}</p>
                                <span className="information-card-link">
                                    {post.linkText}
                                    <i className="fa-solid fa-arrow-right"></i>
                                </span>
                            </div>
                        </a>
                    ))}
                </div>
            </main>
        </div>
    );
}

export default InformationPage;