var app = angular.module('Canyonero', [
    'ngRoute', 
    'ngMaterial'
]);

app.config(function ($routeProvider, $locationProvider) {
//    $locationProvider.html5Mode(true).hashPrefix('!');
    return $routeProvider.when('/', {
        templateUrl: "app/cluster.html",
        controller: 'ClusterCtrl'
    });
});