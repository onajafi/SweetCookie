
var casper = require('casper').create();
var x = require('casper').selectXPath;
var fs = require('fs');

// var output_dic = {"salam":{"num1":10,"num2":20,"num3":30}};

casper.echo('The inputs:');
casper.echo(casper.cli.args[0]);

//reading the input file:
var file_input = fs.read('tmp/'+casper.cli.args[0]);//extract_data_input.json
var parsed_input_JSON = JSON.parse(file_input)

// require('utils').dump(parsed_JSON.pass);
//----------------------

//Init values:
confirmed_score = 10;
unselected_score = -2;
reject_score = -5;


var sample_text = "                   چلو خورشت قیمه بادمجان (1,350 تومان) ";
var sample_2 = "             چلو خورشت قیمه بادمجان    ";
var week_regex = /یک شنبه|دوشنبه|سه شنبه|چهارشنبه|پنج شنبه|جمعه|شنبه/
var date_regex = /[0-9]{4}[/][0-9]{1,2}[/][0-9]{1,2}/
var name_regex = / *([\u0600-\u06FF ]*[\u0600-\u06FF]) */
// var meal_regex = / *([\u0600-\u06FF ]*[\u0600-\u06FF]) *\(.*/
// casper.echo("+++++++++");
// require('utils').dump(sample_text.match(name_regex));
// require('utils').dump(sample_2.match(name_regex));
// casper.echo(sample_2.match(name_regex)[1]);
// casper.echo("+++++++++");
var output_for_JSON = {};

//regex Filters:
function give_clean_meal_name(str1){
    return str1.match(name_regex)[1];
}

//NEW
function give_meal_priority_in_row(ref,row_num){
    lunch_block_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > td:nth-child(2)';
    dinner_block_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > td:nth-child(3)';
    date_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > th';
    temp_output = {};


    //LUNCH
    lunch_arr = [];
    if(ref.exists(lunch_block_selector)) {
        ref.echo(ref.getElementInfo(lunch_block_selector).text);
        for(var i=1;;i++) {
            meal_selector = lunch_block_selector + '> div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + i + ')';
            if (ref.exists(meal_selector)) {
                var temp_meal = {};
                meal_dat = ref.getElementInfo(meal_selector);
                ref.echo("++++" + i);
                ref.echo(meal_dat.text);
                temp_meal["meal_name"] = give_clean_meal_name(meal_dat.text);

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
                lunch_arr.push(temp_meal);
            }else {
                break;
            }
        }
    }else{
        // ref.echo("INCORRECT ROW NUMBER: " + row_num);
        ref.echo("EMPTY LUNCH ROW: " + row_num)
    }
    // Process the ordered lunch:
    var chosen_ST = false;
    for(var i=0;i<lunch_arr.length;i++) {
        temp_meal = lunch_arr[i];
        if (temp_meal["status"] == "OK_DONE" ||
                temp_meal["status"] == "OK_AWAITING"){
            chosen_ST = true;
            break;
        }
    }
    for(var i=0;i<lunch_arr.length;i++) {

        temp_meal = lunch_arr[i];
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

    return temp_output;
}

function get_ALL_priority_in_table(ref){
    var priorities = {};
    for(var j=1;j<=7;j++){
        ref.echo('================');
        var pri = give_meal_priority_in_row(ref,j);
        //merging the result to the main dictionary:
        for(var key in pri){
            if(key in priorities){
                priorities[key] = priorities[key] + pri[key];
            }else{
                priorities[key] = pri[key];
            }
        }
    }
    return priorities;
}

function navigate_to_previous_week(ref){

    //Get a data to compare and make sure the new page has been loaded
    date_selector = 'div.reserve-table > table.table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(1) > th:nth-child(1)';
    tmp_OBJ = ref.getHTML(date_selector);
    ref.echo(tmp_OBJ);

    ref.thenClick('div.reserve-table > div.has-bottom-margin:nth-child(1) > div:nth-child(2) > div:nth-child(3) > button:nth-child(1)')

    check_FUNC = function (tries) {

        if(tmp_OBJ != ref.getHTML(date_selector)){
            ref.echo("Got in the new previous table");
            return;
        }else{
            ref.echo("One fail, trying again...");
            ref.wait(100,check_FUNC,tries - 1);
        }



        if(tries==0 && tmp_OBJ == this.getHTML(date_selector)){
            ref.echo("DIDN'T get in...");
            return;
        }

    }

    ref.wait(100,check_FUNC,40)

    return;
}

function get_ALL_priority_in_previous_weeks(ref,number_of_weeks){
    var priorities = {};

    function PRIinWEEK() {
            for (var j = 1; j <= 7; j++) {
                ref.echo('================');
                var pri = give_meal_priority_in_row(ref, j);
                //merging the result to the main dictionary:
                for (var key in pri) {
                    if (key in priorities) {
                        priorities[key] = priorities[key] + pri[key];
                    } else {
                        priorities[key] = pri[key];
                    }
                }
            }
        }

    for(var week=0;week<number_of_weeks;week++) {

        //extracting the data:
        ref.then(PRIinWEEK);

        //load the new table:
        if(week < number_of_weeks - 1){//check if the new table is necessary to load
            ref.then(function(){
                navigate_to_previous_week(this);
            })
        }
    }
    return priorities;
}

//DATA extract:
function give_ALL_THE_data_in_row(ref,row_num){
    lunch_block_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > td:nth-child(2)';
    dinner_block_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > td:nth-child(3)';
    date_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > th';
    temp_output = {};
    if(ref.exists(date_selector)){
        // ref.echo(ref.getElementInfo(date_selector).text);
        ref.echo(ref.getElementInfo(date_selector).text.match(week_regex));
        ref.echo(ref.getElementInfo(date_selector).text.match(date_regex));
        temp_output["day"] = ref.getElementInfo(date_selector).text.match(week_regex)[0];
        temp_output["date"] = ref.getElementInfo(date_selector).text.match(date_regex)[0];
    }
    else{
        temp_output["day"] = "";
        temp_output["date"] = "";
    }

    temp_output["lunch_arr"] = [];
    if(ref.exists(lunch_block_selector)) {
        ref.echo(ref.getElementInfo(lunch_block_selector).text);
        for(var i=1;;i++) {
            meal_selector = lunch_block_selector + '> div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + i + ')';
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
                temp_output["lunch_arr"].push(temp_meal);
            }else {
                break;
            }
        }
    }else{
        // ref.echo("INCORRECT ROW NUMBER: " + row_num);
        ref.echo("EMPTY LUNCH ROW: " + row_num)
    }

    temp_output["dinner_arr"] = [];
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
                temp_output["dinner_arr"].push(temp_meal);
            }else {
                break;
            }
        }
    }else{
        // ref.echo("INCORRECT ROW NUMBER: " + row_num);
        ref.echo("EMPTY DINNER ROW: " + row_num)
    }

    return temp_output;
}

function give_ALL_THE_data_in_table(ref){
    var table_output=[];
    for(var j=1;j<=7;j++){
        ref.echo('================');
        table_output.push(give_ALL_THE_data_in_row(ref,j));
    }
    return table_output
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

function extract_json_file(){
    var output_filename = 'output_PRI_'+parsed_input_JSON.chat_id + '.json';
    fs.write('tmp/'+output_filename, JSON.stringify(output_for_JSON), 'w');
}

casper.start('http://dining.sharif.edu/login');

var tmp_OBJ,tmp_DIC;

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
        // scrape something
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
    .then(function(){
        for(var i=0;i<5;i++) {//wait for 10 secs in total
            this.wait(1000);
            if(this.exists('div.fast_access_container')){
              break;
            }
        }
    })
    .then(function(){
        // scrape something else
        this.echo(this.getTitle());
        if(this.exists('div.fast_access_container')) {
            this.echo(this.getHTML('div.fast_access_container'));
            output_for_JSON["PASSWORD_STATE"] = "CORRECT";
        }else{
            output_for_JSON["PASSWORD_STATE"] = "WRONG";
            this.capture('navigation123.png');
            this.echo("Got a wrong pass SIG...");
            extract_json_file();
            this.exit();
        }
    })
    .thenOpen("http://dining.sharif.edu/admin/food/food-reserve/reserve")
    // .then(function() { TODO uncomment this at the end
    //     this.evaluate(function (row_value) {
    //         var form = document.querySelector('select#foodreservesdefineform-self_id');
    //         form.selectedIndex = row_value;
    //         $(form).val(row_value).change();
    //
    //     }, parsed_input_JSON["PLCnum"]);
    // })
    // .then(function(){
    //     for(var i=0;i<10;i++) {//wait for 10 secs in total
    //       // this.waitFor(1000);
    //       this.echo('324234waiting');
    //       if(this.exists()){
    //           break;
    //       }
    //   }
    // })
    .waitForSelector('div.reserve-table > div.has-bottom-margin:nth-child(1) > div:nth-child(2) > div:nth-child(3) > button:nth-child(1)')
    // .thenClick('div.reserve-table > div.has-bottom-margin:nth-child(1) > div:nth-child(2) > div:nth-child(3) > button:nth-child(1)')
    // .then(function(){
    //     this.wait(4000, function(){this.echo('Waiting finished')});
    // })
    // .then(function(){
    //     navigate_to_previous_week(this);
    // })
    .then(function(){
        tmp_DIC = get_ALL_priority_in_previous_weeks(this,10);
    })
    .then(function(){// Sorting
        // Create items array
        var items = Object.keys(tmp_DIC).map(function(key) {
          return [key, tmp_DIC[key]];
        });

        // Sort the array based on the second element
        items.sort(function(first, second) {
          return second[1] - first[1];
        });

        for(var i=0;i<items.length;i++) {
            this.echo(items[i]);
        }
        output_for_JSON["Priority"] = items;
    })
    .then(function(){


        this.capture('navigation.png');

        extract_json_file();
    });

casper.run();
