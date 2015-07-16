app.controller("ClusterCtrl", ['$scope', 
function ($scope) {
    window.s = $scope;
    $scope.placeholderCanonical = "Pfizer, inc.";
    $scope.placeholderList = {
      included: [ "Pfizer inc", "Pfizer labs" ],
      excluded: [ "Pfizer Health Consolidated inc", "The Pfizer labs" ]
    };
    $scope.placeholderListLast = $scope.placeholderListOrig = angular.copy($scope.placeholderList);
    $scope.undoDisabled = true; 

    $scope.exclude = function(item) {
      // capture previous state for undo
      $scope.placeholderListLast = angular.copy($scope.placeholderList);
      // put it in included list
      $scope.placeholderList.excluded.push(item);
      // find it in the excluded list and remove
      var index = $scope.placeholderList.included.indexOf(item);
      $scope.placeholderList.included.splice(index, 1); 
      $scope.undoDisabled = false; 
    };

    $scope.include = function(item) {
      // capture previous state for undo
      $scope.placeholderListLast = angular.copy($scope.placeholderList);
      // put it in included list
      $scope.placeholderList.included.push(item);
      // find it in the excluded list and remove
      var index = $scope.placeholderList.excluded.indexOf(item);
      $scope.placeholderList.excluded.splice(index, 1);  
      $scope.undoDisabled = false;
    };

    $scope.undo = function() {
      console.log('undo');
      $scope.placeholderList = angular.copy($scope.placeholderListLast);
      $scope.undoDisabled = true;
    };

    $scope.reset = function() {
      $scope.placeholderList = angular.copy($scope.placeholderListOrig);
    }

}]);