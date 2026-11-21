const searchBar = document.getElementById("search-bar");
const articleContent = document.getElementById("article-content");

let wikiIndex = {};

// 1. Direct function to display article content from our in-memory index
function loadArticleContent(contentKey) {
  // Look up the content directly from the loaded JSON, fallback if missing
  const content = wikiIndex[contentKey] || "<p>Article not found.</p>";
  articleContent.innerHTML = content;
}

// 2. Run when the page first loads
window.addEventListener("DOMContentLoaded", async () => {
  // Load default welcome/standard page message or check if you have a "welcome" key in your JSON
  articleContent.innerHTML = "Welcome to the E.R.I.P. wiki!";

  // Fetch index.json (which now contains title -> raw HTML text string)
  try {
    const response = await fetch("index.json");
    wikiIndex = await response.json();
  } catch (error) {
    console.error("Could not load index.json:", error);
  }
});

// 3. Listen for typing in the search bar
searchBar.addEventListener("input", () => {
  const query = searchBar.value.trim().toLowerCase();

  // If search bar is cleared, go back to default welcome text
  if (query === "") {
    articleContent.innerHTML = "Welcome to the E.R.I.P. wiki!";
    return;
  }

  // Find all keys in index.json that contain the search text
  const matchingKeys = Object.keys(wikiIndex).filter((key) =>
    key.toLowerCase().includes(query)
  );

  // Case 0: No results
  if (matchingKeys.length === 0) {
    articleContent.innerHTML = "<p>no results found</p>";
  } 
  // Case 1: Exactly one match -> load that article text directly
  else if (matchingKeys.length === 1) {
    loadArticleContent(matchingKeys[0]);
    searchBar.value = "";
  } 
  // Case 2+: Multiple matches -> display clickable links
  else {
    articleContent.innerHTML = "<h3>Multiple results found:</h3><ul id='results-list'></ul>";
    const list = document.getElementById("results-list");

    matchingKeys.forEach((key) => {
      const li = document.createElement("li");
      const link = document.createElement("a");
      link.href = "#";
      link.textContent = key;

      // Load the clicked article content when selected
      link.addEventListener("click", (e) => {
        e.preventDefault();
        loadArticleContent(key);
        searchBar.value = "";
      });

      li.appendChild(link);
      list.appendChild(li);
    });
  }
});

// 4. Listen for clicks inside the article content area to catch internal wiki links
articleContent.addEventListener("click", (e) => {
  const wikiLink = e.target.closest("a[data-article]");
  
  if (wikiLink) {
    e.preventDefault();
    const articleTitle = wikiLink.getAttribute("data-article");
    
    if (wikiIndex.hasOwnProperty(articleTitle)) {
      loadArticleContent(articleTitle);
      searchBar.value = "";
    } else {
      console.error("Article not found in index.json:", articleTitle);
    }
  }
});