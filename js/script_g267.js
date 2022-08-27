// Dark Mode

const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
const currentTheme = localStorage.getItem('theme');

if (currentTheme) {
    document.documentElement.setAttribute('data-theme', currentTheme);
  
    if (currentTheme === 'dark') {
        toggleSwitch.checked = true;
    }
}

function switchTheme(e) {
    if (e.target.checked) {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    }
    else {        
    	document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
    }    
}

toggleSwitch.addEventListener('change', switchTheme, false);

// Iterate through divs

$(document).ready(function(){

	var params = new window.URLSearchParams(window.location.search); // Récupère tous les paramètres de l'URL
	var myCurrentSection = params.get('id'); // Met dans une variable un paramètre en particulier
	
	// Affichage de la section courante
	var myImageDiv = '#myImage'+ myCurrentSection; // Crée une chaîne de caractères
	var myTextDiv = '#myText'+ myCurrentSection;
	$(myImageDiv).show(); // JQuery appelle la section correspondante à partir de la nouvelle chaîne de caractères
	$(myTextDiv).show();
	
	// Modifier l'URL du bouton previous
	var myPreviousSection = parseInt(myCurrentSection) - 1;
	var urlPrevious = "g267.html?id=" + myPreviousSection;
	$("#previous").attr("href", urlPrevious);
		
	// Modifier l'URL du bouton next
	var myNextSection = parseInt(myCurrentSection) + 1;
	var urlNext = "g267.html?id=" + myNextSection;
	$("#next").attr("href", urlNext);
});