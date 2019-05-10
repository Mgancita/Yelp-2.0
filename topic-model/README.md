# Topic Modeling and Polarity

Gensim's LDA was used to create the topic model for this project. 

<h2> Training </h2>

The actual LDA model is in the model_data folder. It is trained for seven topics on the reviews from yelp's data dump. 

<href> https://www.yelp.com/dataset </href> 

The train_model script allows the user to either create their own model, or to use the current dictionary and corpus from the project to create another LDA model with a different topic parameter. 


<b> <em>To adjust the LDA model: </em> </b> 

>The dictionary can be found in the model_data folder. The corpus was too large to push, Download it from the google drive link [here](https://drive.google.com/open?id=1kAQS4Nn38IwUmXBxTMwOUd-q8yiReqcJ)



<h2>  Testing </h2>

The topic testing phase of this project generates topics related to each review and calculates their respective polarity score. 


<h5> Example </h5> 
Given a review:

> “The best food the best place to eat chicken and waffles on a slow day. However this was my first time back to the deli since moving back to the area.”

<dl >
<dd> The review is split into sentences, and for each sentence LDA generates  the probability of the topics related to the sentence, and a ranked list of the topics associated to the words in descending order. Our topic / polarity model only looks into the first topic in the ranked list.</dd> 
</dl>

>> If a filter is specified, (in our case 14%), only the topics  above the threshold and their corresponding words will be taken into consideration. 

| Topics Associated to the Sentence |   | Topics Associated to Words in the Sentence |
|-----------------------------------|---|--------------------------------------------|
| [(0, 0.06013425),                 |   | [(0, [<strong><em>2</em> </strong>]),                                 |
| <strong><em>(1, 0.20457779) </em></strong>,                  |   | (1, [<strong><em>2</em></strong>, 3]),                               |
| <strong><em>(2, 0.30940828)</em></strong>,                  |   | (2, [<strong><em>1</em></strong>, 0, 3,]),                           |
| (3, 0.02120836),                  |   | (3, [<strong><em>2</em></strong>, 0]),                               |
| <strong><em>(4, 0.143796033)</em></strong>,                 |   | (4, [<strong><em>1</em></strong>, 2]),                               |
| (5, 0.05160969),                  |   | (5, [<strong><em>1</em></strong>, 5]),                               |
| (6, 0.01121853)]                  |   | (6, [<strong><em>2</em></strong>, 4]),                                  |
|                                   |   | (7, [3])]  | 


The number representation of the words are matched back to the dictionary to get the keys which in turn are paired with the tokenized sentence to create sub sentences. These sentences are then used to calculate the polarity for the topic. 

<p align="center"> 
[<em> ( 1, [ 2,4,5 ] ) </em>, <strong>( 2, [ 0,1,3,6 ] ) </strong>] 
</p> 

  <h3 align = "center">&mapstodown; </h3>  

<p align="center"> 
{<strong>'best': 0</strong>, <strong>'food': 1</strong>, <em>'place': 2 </em>,<strong> 'eat': 3</strong>, <em>'chicken': 4</em>,<em> 'waffles': 5</em>, <strong>'slow': 6</strong>, 'day': 7}
</p> 

<h3 align = "center">&mapstodown; </h3>

<p align="center"> 
[<strong>'best'</strong>, <strong>'food'</strong>,<strong> 'best'</strong>, <em> 'place'</em> , <strong>'eat'</strong>,<em> 'chicken'</em> ,<em>  'waffles'</em> , <strong>'slow'</strong>, 'day']
</p> 

<h3 > &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&mapstodown; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &mapstodown;</h3>


<center>

| | |
|-------------------------|---------------------------|
| <strong>“place chicken waffles” </strong>|<em> “best food best eat slow” </em>|
| 0.1                     | 0.5666666666666667        |

</center>

The steps above are repeated for each sentence within a review. 

<p align="center"> 
{0: [], 1: [0.1], 2: [0.5666666666666667 ,0.27499999999999997, 0.0], 3: [], 4: [], 5: [], 6: []}  
</p> 

The average of the values are taken to get an overall polarity score for the review. 

<p align="center"> 
{‘Order Selection': 0.1, ‘Location’: 0.42}
</p>



>>The polarity scores can also be grouped by restaurant Id's and used to calculate each respective restaurant's polarity score. 



 
