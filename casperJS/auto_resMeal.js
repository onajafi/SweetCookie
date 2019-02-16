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

function Confirm_the_click(ref,CSSselector,tries) {
    if(tries <= 0){
        ref.click
        return;
    }
    if(ref.exists(CSSselector)){
        ref.wait(100,Confirm_the_click,ref,CSSselector,tries-1);
    }
    return;
}

//Get stuff like the users name, and account credit balance
function get_balance_info(ref){
    credit_balance_selector = 'span.main_balance_span.balance_negative';
    if(ref.exists(credit_balance_selector)) {
        ref.echo(parseFloat(ref.getElementInfo(credit_balance_selector).text.replace(",", ".")));
        return parseFloat(ref.getElementInfo(credit_balance_selector).text.replace(",", "."));
    }
    else{//Looks like the balance is positive $_$
        credit_balance_selector = 'span.main_balance_span';
        if(ref.exists(credit_balance_selector)) {
            ref.echo(parseFloat(ref.getElementInfo(credit_balance_selector).text.replace(",", ".")));
            return parseFloat(ref.getElementInfo(credit_balance_selector).text.replace(",", "."));
        }
    }
    return -1;
}

// This function orders the dinner and lunch in the row of a table
// row_num: The row number in the table [1...7]
// get_lunch: If true it will reserve the meal at that time, otherwise it will just skip that part
// get_dinner: Same as get_lunch but for dinner
function order_in_row(ref,row_num,get_lunch,get_dinner){
    lunch_block_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > td:nth-child(2)';
    dinner_block_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > td:nth-child(3)';
    date_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > th';

    var meal_num_with_max_point = 0;
    var max_point;
    var res_state = "NO_MEAL";
    var meal_CNT = 0;

    //LUNCH
    if(!get_lunch){
        ref.echo("DECIDED NOT TO ORDER LUNCH ROW: " + row_num)
    }else if(ref.exists(lunch_block_selector)) {
        // ref.echo(ref.getElementInfo(lunch_block_selector).text);
        for(var i=1;;i++) {
            meal_selector = lunch_block_selector + '> div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + i + ')';
            if (ref.exists(meal_selector)) {
                if(!(ref.exists(meal_selector + '> span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip'))){
                    res_state = "CANT_GET";
                    break;
                }
                meal_CNT++;
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

                if(res_state != "UNKNOWN_MEAL") {//TODO check the else
                    if (meal_num_with_max_point == 0) {//initial value
                        max_point = name_to_point_map[MEAL_name];
                        meal_num_with_max_point = i;
                        res_state = "GOOD_TO_GO";
                    } else if (max_point < name_to_point_map[MEAL_name]) {
                        max_point = name_to_point_map[MEAL_name];
                        meal_num_with_max_point = i;
                    } else if (max_point == name_to_point_map[MEAL_name]) {//We have a problem here...
                        res_state = "EQUAL_POINTS";
                    }
                } else {
                    meal_num_with_max_point = 1;
                }
            }else {
                break;
            }
        }
        //Now we're going to select the order button
        if(res_state == "GOOD_TO_GO" || (res_state == "UNKNOWN_MEAL" && meal_CNT == 1)){
            res_selector = lunch_block_selector + '> div.food-reserve-diet-div.has-mini-bottom-padding:nth-child('
                + meal_num_with_max_point + ')'
                + '> span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip';
            ref.click(res_selector);
        }
        ref.echo(res_state);
    }else{
        // ref.echo("INCORRECT ROW NUMBER: " + row_num);
        ref.echo("EMPTY LUNCH ROW: " + row_num)
    }



    meal_num_with_max_point = 0;
    res_state = "NO_MEAL";
    meal_CNT = 0;

    //DINNER
    if(!get_dinner){
        ref.echo("DECIDED NOT TO ORDER DINNER ROW: " + row_num)
    }else if(ref.exists(dinner_block_selector)) {
        // ref.echo(ref.getElementInfo(dinner_block_selector).text);
        for(var i=1;;i++) {
            meal_selector = dinner_block_selector + '> div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + i + ')';
            if (ref.exists(meal_selector)) {
                if(!(ref.exists(meal_selector + '> span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip'))){
                    res_state = "CANT_GET";
                    break;
                }
                meal_CNT++;
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

                if(res_state != "UNKNOWN_MEAL") {
                    if (meal_num_with_max_point == 0) {//initial value
                        max_point = name_to_point_map[MEAL_name];
                        meal_num_with_max_point = i;
                        res_state = "GOOD_TO_GO";
                    } else if (max_point < name_to_point_map[MEAL_name]) {
                        max_point = name_to_point_map[MEAL_name];
                        meal_num_with_max_point = i;
                    } else if (max_point == name_to_point_map[MEAL_name]) {//We have a problem here...
                        res_state = "EQUAL_POINTS";
                    }
                } else {
                    meal_num_with_max_point = 1;
                }

            }else {
                break;
            }
        }
        //Now we're going to select the order button
        if(res_state == "GOOD_TO_GO" || (res_state == "UNKNOWN_MEAL" && meal_CNT == 1)){
            res_selector = dinner_block_selector + '> div.food-reserve-diet-div.has-mini-bottom-padding:nth-child('
                + meal_num_with_max_point + ')'
                + '> span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip';
            ref.thenClick(res_selector);
        }
        ref.echo(res_state);
    }else{
        // ref.echo("INCORRECT ROW NUMBER: " + row_num);
        ref.echo("EMPTY DINNER ROW: " + row_num)
    }

    return;
}

//Check if a meal is ordered in a row:
function check_in_row(ref,row_num,get_lunch,get_dinner){
    lunch_block_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > td:nth-child(2)';
    dinner_block_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > td:nth-child(3)';
    date_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > th';


    //LUNCH
    if(!get_lunch){
        ref.echo("DECIDED NOT TO CHECK LUNCH ROW: " + row_num)
    }else if(ref.exists(lunch_block_selector)) {
        for(var i=1;;i++) {
            meal_selector = lunch_block_selector + '> div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + i + ')';
            if (ref.exists(meal_selector)) {
                // If the shopping cart exists in the row it means it has a
                if(ref.exists(meal_selector + '> span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip')){
                    return false;// IT'S NOT SELECTED!!!
                }
                break;// It is selected...
            } else {
                break;
            }
        }
    }else{
        ref.echo("EMPTY LUNCH ROW: " + row_num)
    }



    meal_num_with_max_point = 0;
    res_state = "NO_MEAL";
    meal_CNT = 0;

    //DINNER
    if(!get_dinner){
        ref.echo("DECIDED NOT TO CHECK DINNER ROW: " + row_num)
    }else if(ref.exists(dinner_block_selector)) {
        // ref.echo(ref.getElementInfo(dinner_block_selector).text);
        for(var i=1;;i++) {
            meal_selector = dinner_block_selector + '> div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + i + ')';
            if (ref.exists(meal_selector)) {
                if(ref.exists(meal_selector + '> span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip')){
                    return false;
                }
                break;
            } else {
                break;
            }
        }
    }else{
        // ref.echo("INCORRECT ROW NUMBER: " + row_num);
        ref.echo("EMPTY DINNER ROW: " + row_num)
    }

    return true;
}

//Having some problems in the type of what we parse in "serve_times" so I made this function:
function include(array,elem){
    count = array.length;
    for (i=0;i<count;i++){
        if(array[i] == elem)
            return true;
    }
    return false;
}

function order_all_meals_in_table(ref){
    var temp_SERVE_TIME = parsed_input_JSON["serve_times"];
    ref.echo(temp_SERVE_TIME);
    for (var j = 1; j <= 7; j++) {
        ref.echo('================'+j);

        if(include(temp_SERVE_TIME,j)){
            get_lunch = true;
            ref.echo("TRUE_LUNCH");
        }else{
            get_lunch=false;
        }

        if(include(temp_SERVE_TIME,j+7)){
            get_dinner = true;
        }else{
            get_dinner=false;
        }

        if(get_lunch || get_dinner) {
            order_in_row(ref, j, get_lunch, get_dinner);
            ref.echo("CALLED_THE_FUNC");
        }
    }
    return true;
}

function check_all_meal_order(ref){
    var temp_SERVE_TIME = parsed_input_JSON["serve_times"];
    ref.echo(temp_SERVE_TIME);
    for (var j = 1; j <= 7; j++) {
        ref.echo('================'+j);

        if(include(temp_SERVE_TIME,j)){
            get_lunch = true;
        }else{
            get_lunch=false;
        }

        if(include(temp_SERVE_TIME,j+7)){
            get_dinner = true;
        }else{
            get_dinner=false;
        }

        if(get_lunch || get_dinner) {
            if(!check_in_row(ref, j, get_lunch, get_dinner)){
                return false;//We have a missed item here :/
            }
        }
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
.thenClick('.navigation-link:nth-child(1)')// Uncomment this part before release (to navigate next week)
.then(function(){
    this.wait(3000, function(){this.echo('Waiting finished')});
})
.then(function(){
    order_all_meals_in_table(this);
})
//.thenOpen("http://dining.sharif.edu/admin/food/food-reserve/reserve")
.then(function(){
    this.wait(3000, function(){this.echo('Waiting finished')});
})
.then(function(){
    this.capture('navigation_DBG.png');
    check_res = check_all_meal_order(this);//True means OK
    output_for_JSON["ORDERED_MEALS_STAT"] = check_res;
})
.then(function(){
    // scrape something else
    //this.echo(this.getTitle());
    //this.echo(this.getHTML('[class="table sharif-table table-bordered table-condensed"]'));
    this.echo("_________________________________________________");
    this.capture('navigation.png');
    output_for_JSON["Balance"] = get_balance_info(this);
    extract_json_file();
    // this.echo(this.getHTML(x("//body//form")));
    //this.echo(this.getHTML(x("//body//form//div[class='reserve-table']")));
});

casper.run();
