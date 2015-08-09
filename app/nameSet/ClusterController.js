app.controller("ClusterController", ['$scope', 
function ($scope) {
    var s = $scope;

    fetchItem = function() {
      // hard coded cluster object (to be replaced in show w/ real service call)
      s.cluster = {
        id: 12345,
        canonicalName: "Pfizer, inc.",
        included: [ "Pfizer inc", "Pfizer labs" ],
        excluded: [ "Pfizer Health Consolidated inc", "The Pfizer labs" ]
      }
      initHistory();
    };

    initHistory = function() {
      // clear it out
      s.clusterHistory = [];
      // add the current state as first item
      captureHistory();
    };

    captureHistory = function() {
      s.clusterHistory.push(angular.copy(s.cluster));
    };

    s.exclude = function(item) {
      move(item, s.cluster.included, s.cluster.excluded);
    };

    s.include = function(item) {
      move(item, s.cluster.excluded, s.cluster.included);
    };

    move = function(item,from_array,to_array) {
      // add to target
      to_array.push(item);
      // find & remove it from source
      from_array.splice( from_array.indexOf(item), 1);
      // capture state for undo
      captureHistory();
    };

    s.checkCanonicalName = function() {
      var oldName = s.clusterHistory[s.clusterHistory.length-1].canonicalName;
      if ( s.cluster.canonicalName !== oldName ) {
        captureHistory();
      }
    }

    s.undo = function() {
      // set the cluster to the previous item from the history 
      // (and pop removes it from history)
      s.clusterHistory.pop();
      s.cluster = angular.copy(s.clusterHistory[s.clusterHistory.length-1]);
    };

    s.undoDisabled = function(){ 
      return (s.clusterHistory.length===1); 
    }; 

    s.reset = function() {
      $scope.cluster = angular.copy($scope.placeholderListOrig);
    }

    s.done = function() {
      // TODO - write data back to server
      //      - fetch next
    }

    // get the data
    fetchItem();

}]);