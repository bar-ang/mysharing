
        function dictsearch(dict, word){
          for(t=0;t<dict.length;t++){
            if(dict[t].word == word)
              return true;
          }
          return false;
        }

        var app = angular.module("dictionary", ['ngSanitize']);
        app.controller("myCtrl", function($scope, $http){
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

            $scope.applyFilter = function(str){
            	$http.get("filtertable.nf?filter=" + str).then(function(response){
                	$scope.entries = response.data;
	            }, function error(response){
	                $scope.error = "Error.";
	            });
            }

            $scope.MarkedText = function(){
                var words = $scope.freeText.split(' ');
                var marked = "";
                for(i=0;i<words.length;i++){
                  stem = words[i].substring(0,words[i].length-1);
                  if(dictsearch($scope.entries,words[i]) || dictsearch($scope.entries,stem))
                    marked += "<span class='marked'>" + words[i] + "</span> ";
                  else
                    marked += words[i] + " ";
                }

                return marked;
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

                $scope.entries.splice($scope.editing, 1);
                $("div.float#editSpace").fadeOut(600);
            }

            $scope.doneEdit = function($index){
                var req = {
					method: 'POST',
					url: "edittuple.nf",
					headers : {
						'Content-Type' : 'application/json'
					},
					data: JSON.stringify(JSON.stringify($scope.entries[$index]))
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

$(document).ready(function() {
	$("div.float").hide();
	//$("div.hinter").show();
})