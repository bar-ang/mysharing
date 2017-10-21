function dictsearch(dict, word){
	for(t=0;t<dict.length;t++){
		if(dict[t].word == word)
			return true;
	}
	return false;
}

function stem(str, suffixes){
	//remove trailing signs like dots, commas, question marks etc.
	word = str.replace(/^[^a-zA-z]+/g,"");
	word = word.replace(/[^a-zA-z]+$/g,"");

	suffix = word.substr(word.length - 1)

	if(suffixes.indexOf(suffix) >= 0){
		return {
			stem: word.substr(0, word.length - 1),
			suffix: word.substr(word.length - 1)
		};
	}else{
		return {
			stem: word,
			suffix: null
		};
	}
}
