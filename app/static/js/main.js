(function(window) {
    // Register an application main module
    var todoapp = window.angular.module('todoapp', []);
    // Register the controller
    // window.angular.module('todoapp')
    todoapp.controller('maincontroller', ['$scope', function($scope) {
        // The role of $scope is to add elements to the view
        // Value in the text box
        $scope.text = ''; // Two-way binding data type will be used

        // To facilitate page display, manually add a list of lists
        $scope.todolist = [];

        // Add function to respond to interaction
        $scope.add = function() {
            var text = $scope.text.trim();
            if (text) {
                $scope.todolist.push({
                    text: text,
                    done: false
                });
                $scope.text = '';
            }
        }

        // Click the response event of the delete button
        $scope.delete = function(todo) {
            var index = $scope.todolist.indexOf(todo)
            $scope.todolist.splice(index, 1); // plays the role of deletion
        }


        // Get the number of completed events, according to whether the checkbox is selected or not
        // Since the page changes dynamically, you need to use functions, or simply use model binding, but that will be a little troublesome
        $scope.doneCount = function() {
            // Use filter to achieve
            var temp = $scope.todolist.filter(function(item) {
                return item.done; // Return true to indicate that the current data meets the conditions and the event has been completed
            });
            return temp.length;
        }
    }]);

})(window)