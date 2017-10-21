var mainApp = angular.module("dictionary", ['ngSanitize']);
var sentenceApp = angular.module("sentence", ['ngSanitize']);

mainApp.controller("myCtrl", function($scope, $http){
    $http.get("gettable.nf").then(function(response){
        $scope.entries = response.data;
    }, function error(response){
        $scope.error = "Error.";
    });

    $scope.addEntry = function(){

      var ans = "no";

       


        var req = {
			method: 'POST',
			url: "addentry.nf",
			headers : {
				'Content-Type' : 'application/json'
			},
			data: JSON.stringify(JSON.stringify($scope.new))
		};

		$http(req).then(function(response){
      	  	ans = response.data;
      	}, function error(response){
       		$scope.error = "Error.";
      	});

      ans = "OK";
      if(ans != "OK"){
        $scope.error = ans;
        return;
      }
      jnew = JSON.parse(JSON.stringify($scope.new));
      $scope.entries.push(jnew);

       $scope.new.word="";
       $scope.new.POS="";
       $scope.new.meaning="";
       $scope.new.translation="";
       $scope.new.english="";
       $scope.new.synonym=1;

       $scope.error = "All Good";
    }

    $scope.applyFilter = function(str, filterType){
    	if(filterType == "startby"){
        	$http.get("filtertable.nf?filter=" + str).then(function(response){
            	$scope.entries = response.data;
            }, function error(response){
                $scope.error = "Error.";
            });
    	}else if(filterType == "regex"){
    		$http.get("filterregextable.nf?filter=" + str).then(function(response){
            	$scope.entries = response.data;
            }, function error(response){
                $scope.error = "Error.";
            });
    	}
    }

    $scope.editing = -1;

    $scope.edit = function($index){
        $scope.editing = $index;
        $("div.float#editSpace").fadeIn(600);
    }

    $scope.removeEntry = function(index){
        query = "?";
        query += "word=" + $scope.entries[index].word;
        $http.get("remtuple.nf" + query).then(function(response){
          ans = response.data;
        }, function error(response){
          $scope.error = "Error.";
        });
        $("div.float#editSpace").fadeOut(600);
        $("table#maintable tr:eq(" + (index+1) + ")").hide(600, function(){
        	$scope.entries.splice($scope.editing, 1);
        });
    }

    $scope.doneEdit = function($index){
        var req = {
			method: 'POST',
			url: "edittuple.nf",
			headers : {
				'Content-Type' : 'application/json'
			},
			data: JSON.stringify($scope.entries[$index])
		};

		$http(req).then(function(response){
      	  	ans = response.data;
      	}, function error(response){
       		$scope.error = "Error.";
      	});

      ans = "OK";
      if(ans != "OK"){
        $scope.error = ans;
        return;
      }




        $("div.float#editSpace").fadeOut(600);
    }
});


sentenceApp.controller("sentCtrl", function($scope, $http){
	$scope.MarkedText = function(){
		var words = $scope.freeText.split(' ');
        var marked = ":)";
        for(i=0;i<words.length;i++){
        	stem = stem(words[i],["a","e","i","o","u","y"]);
			$http.get("translateword.nf?word=" + stem.stem + "&suff=" + stem.suffix).then(function(response){
	      	  	ans = response.data;
	      	  	alert(JSON.stringify(ans));
	      	}, function error(response){
	       		$scope.error = "Error.";
	      	});
        }

        return marked;
    }
});



//~~~~~jQuery~~~~~~~~~
$(document).ready(function() {
	$("div.float").hide();
	$("div.hinter").hide();
})



