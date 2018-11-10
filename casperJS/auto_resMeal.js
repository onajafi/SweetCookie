var casper = require('casper').create();
var fs = require('fs');

casper.echo('The inputs:');
casper.echo(casper.cli.args[0]);

//reading the input file:
var file_input = fs.read('../tmp/'+casper.cli.args[0]);
var parsed_input_JSON = JSON.parse(file_input);
var name_to_point_map = parsed_input_JSON["pri_list"];
// require('utils').dump(parsed_JSON.pass);
//----------------------
var name_regex = / *([\u0600-\u06FF ]*[\u0600-\u06FF]) */

var output_for_JSON = {};

//regex Filters:
function give_clean_meal_name(str1){
    return str1.match(name_regex)[1];
}

function order_in_row(ref,row_num){
    lunch_block_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > td:nth-child(2)';
    dinner_block_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > td:nth-child(3)';
    date_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > th';

    var meal_num_with_max_point = 0;
    var max_point;
    var res_state = "NO_MEAL";

    //LUNCH
    lunch_arr = [];
    if(ref.exists(lunch_block_selector)) {
        // ref.echo(ref.getElementInfo(lunch_block_selector).text);
        for(var i=1;;i++) {
            meal_selector = lunch_block_selector + '> div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + i + ')';
            if (ref.exists(meal_selector)) {
                if(!(ref.exists(meal_selector + '> span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip'))){
                    res_state = "CANT_GET";
                    break;
                }
                meal_dat = ref.getElementInfo(meal_selector);
                ref.echo("++++" + i);
                ref.echo(meal_dat.text);
                MEAL_name = give_clean_meal_name(meal_dat.text);
                if(MEAL_name in name_to_point_map) {
                    ref.echo("point is:");
                    ref.echo(name_to_point_map[MEAL_name]);
                } else {//We have a problem here...
                    ref.echo("Didn't find the name in dictionary:");
                    ref.echo(MEAL_name);
                    res_state = "UNKNOWN_MEAL"
                }

                if(meal_num_with_max_point == 0){//initial value
                    max_point = name_to_point_map[MEAL_name];
                    meal_num_with_max_point = i;
                    res_state = "GOOD_TO_GO";
                } else if(max_point < name_to_point_map[MEAL_name]){
                    max_point = name_to_point_map[MEAL_name];
                    meal_num_with_max_point = i;
                } else if(max_point == name_to_point_map[MEAL_name]){//We have a problem here...
                    res_state = "EQUAL_POINTS";
                }
            }else {
                break;
            }
        }
        //Now we're going to select the order button
        if(res_state == "GOOD_TO_GO"){
            res_selector = lunch_block_selector + '> div.food-reserve-diet-div.has-mini-bottom-padding:nth-child('
                + meal_num_with_max_point + ')'
                + '> span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip';
            ref.thenClick(res_selector);
        }
        ref.echo(res_state);
    }else{
        // ref.echo("INCORRECT ROW NUMBER: " + row_num);
        ref.echo("EMPTY LUNCH ROW: " + row_num)
    }



    return;




    dinner_arr = [];
    if(ref.exists(dinner_block_selector)) {
        ref.echo(ref.getElementInfo(dinner_block_selector).text);
        for(var i=1;;i++) {
            meal_selector = dinner_block_selector + '> div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + i + ')';
            if (ref.exists(meal_selector)) {
                var temp_meal = {};
                meal_dat = ref.getElementInfo(meal_selector);
                ref.echo("++++" + i);
                ref.echo(meal_dat.text);
                temp_meal["meal_name"] = meal_dat.text;

                //Check if it has been reserved:
                if(ref.exists(meal_selector + '> span.fa.fa-check.fa-lg.has-left-margin.has_tooltip')){
                    ref.echo('CONFIRMED!');
                    temp_meal["status"] = "OK_DONE";
                }
                else if(ref.exists(meal_selector + '> span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip')){
                    ref.echo("You can still get it...");
                    temp_meal["status"] = "AWAITING";
                }
                else if(ref.exists(meal_selector + '> span.fa.fa-times-circle.fa-lg.has-left-margin.cursor_pointer.has_tooltip')){
                    ref.echo('Confirmed - But may get canceled...');
                    temp_meal["status"] = "OK_AWAITING";
                }
                else{
                    ref.echo("Nope you lost it!!!");
                    temp_meal["status"] = "FAILED";
                }
                dinner_arr.push(temp_meal);
            }else {
                break;
            }
        }
    }else{
        // ref.echo("INCORRECT ROW NUMBER: " + row_num);
        ref.echo("EMPTY DINNER ROW: " + row_num)
    }
    // Processing dinner:
    var chosen_ST = false;
    for(var i=0;i<dinner_arr.length;i++) {
        temp_meal = dinner_arr[i];
        if (temp_meal["status"] == "OK_DONE" ||
                temp_meal["status"] == "OK_AWAITING"){
            chosen_ST = true;
            break;
        }
    }
    for(var i=0;i<dinner_arr.length;i++) {

        temp_meal = dinner_arr[i];
        switch (temp_meal["status"]) {
            case "OK_DONE":
            case "OK_AWAITING":
                temp_output[temp_meal["meal_name"]] = confirmed_score;
                break;
            case "FAILED":
                if(chosen_ST){
                    temp_output[temp_meal["meal_name"]] = reject_score;
                }else{
                    temp_output[temp_meal["meal_name"]] = unselected_score;
                }
                break;
            case "AWAITING":
                temp_output[temp_meal["meal_name"]] = unselected_score;
                break;
        }
    }

    return;
}


function order_all_meals_in_table(ref){

    for (var j = 1; j <= 7; j++) {
        ref.echo('================');
        order_in_row(ref, j);
    }

    return true;
}

//DATA extract:

function extract_json_file(){
    var output_filename = 'output_ARS_'+parsed_input_JSON.chat_id + '.json';
    fs.write('../tmp/'+output_filename, JSON.stringify(output_for_JSON), 'w');
}

casper.start('http://dining.sharif.edu/login');

casper.then(function() {
    var title = this.getTitle();
    this.echo('First Page: ' + title);
    if(title.search(/سامانه تغذیه/) != -1){
        output_for_JSON["ENTRY_STATE"] = "GOOD";
    }
    else{
        this.echo("Didn't load page");
        output_for_JSON["ENTRY_STATE"] = "BAD";
        extract_json_file();
        this.exit();
    }
})
.then(function(){
    this.echo(parsed_input_JSON["pass"]);
    this.echo(parsed_input_JSON["user"]);
    this.echo(this.sendKeys('input#loginform-username', parsed_input_JSON["user"]));
    this.echo(this.sendKeys('input#loginform-password', parsed_input_JSON["pass"]));
    this.echo(this.getHTML('[class="btn btn-default btn-block"]'));
})
.thenClick('[class="btn btn-default btn-block"]')
.thenOpen("http://dining.sharif.edu/admin/")
.then(function(){
    // scrape something else
    this.echo(this.getTitle());
})
.thenOpen("http://dining.sharif.edu/admin/food/food-reserve/reserve")
.then(function(){
    // scrape something else
    this.echo(this.getTitle());
    if(this.exists('.navigation-link:nth-child(1)')) {
        this.echo(this.getHTML('.navigation-link:nth-child(1)'));
        output_for_JSON["PASSWORD_STATE"] = "CORRECT";
    }else{
        output_for_JSON["PASSWORD_STATE"] = "WRONG";
        extract_json_file();
        this.exit();
    }
})
/*.thenClick('.navigation-link:nth-child(1)')*/
.then(function(){
    for(var i=0;i<10;i++) {//wait for 10 secs in total
      this.wait(1000, function () {});
      if(this.exists('select#foodreservesdefineform-self_id')){
          break;
      }
    }
    this.echo('Waiting finished')
})
.then(function(){//Setting the place
    this.evaluate(function (row_value) {
        var form = document.querySelector('select#foodreservesdefineform-self_id');
        form.selectedIndex = row_value;
        $(form).val(row_value).change();

    }, parsed_input_JSON["PLCnum"]);
})
.then(function(){
    this.wait(3000, function(){this.echo('Waiting finished')});
})
// .thenClick('.navigation-link:nth-child(1)')
// .then(function(){
//     this.wait(3000, function(){this.echo('Waiting finished')});
// })TODO uncomment this part before release (to navigate next week)
// .then(function(){
//     var order_list = parsed_input_JSON["order_list"];
//
//     ref = this;
//     Object.keys(order_list).forEach(function(key) {
//         ref.echo("IN_LOOP:");
//         ref.echo(key);
//         if(order_list[key] == "nevermind"){
//             return;
//         }
//         //Find out if this is a lunch or dinner:
//         var column;
//         if(Number(key) < 7){
//             column = '2';
//             var cart_button_selector = 'tr:nth-child(' + (Number(key) + 1)
//             + ') > td:nth-child('+ column +') > div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + (Number(order_list[key]) + 1)
//             + ') > span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip';
//         }else{
//             column = '3';
//             var cart_button_selector = 'tr:nth-child(' + (Number(key) -6)
//             + ') > td:nth-child('+ column +') > div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + (Number(order_list[key]) + 1)
//             + ') > span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip';
//         }
//
//
//         if(ref.exists(cart_button_selector)) {
//             ref.thenClick(cart_button_selector);
//             ref.echo("FOUND: " + key + " - " + order_list[key])
//         }else{
//             ref.echo("Didn't find the button: " + key + " - " + order_list[key])
//         }
//     });
// })
.then(function(){
    order_all_meals_in_table(this);
})
.then(function(){
    // scrape something else
    //this.echo(this.getTitle());
    //this.echo(this.getHTML('[class="table sharif-table table-bordered table-condensed"]'));
    this.echo("_________________________________________________");
    this.capture('navigation.png');
    extract_json_file();
    // this.echo(this.getHTML(x("//body//form")));
    //this.echo(this.getHTML(x("//body//form//div[class='reserve-table']")));
});

casper.run();
