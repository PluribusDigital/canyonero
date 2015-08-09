var app = angular.module('appCanyonero', [
    'ngRoute', 
    'ngMaterial',
    'ngAnimate'
]);

app.config(function ($routeProvider, $locationProvider) {
//    $locationProvider.html5Mode(true).hashPrefix('!');
    return $routeProvider.when('/', {
        templateUrl: "nameSet/cluster.html",
        controller: 'ClusterController'
    });
});