function printBookmarkStatus(results) {
  // results is either success or error message

  if (results === "You have already bookmarked this recipe.") {
    // error message
    alert(results);
  } else {
    // success message
    alert(results);
  }
}

function handleBookmarkRecipe(evt) {
  var recipeId = $(this).data("recipeId");

  // send info to server; if successful, execute function
  $.post("/bookmark.json", { recipe_id: recipeId }, printBookmarkStatus);
}

// event listener for bookmark button in dashboard.html
$(document).on("click", ".favorite", handleBookmarkRecipe);
