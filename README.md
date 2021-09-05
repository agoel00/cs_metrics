# Metrics for Measuring Code-Switching

Methods Included:
- [x] Code Mixing Index
- [x] Multilingual Index
- [x] Language Entropy
- [x] I-index : Prob of Switching
- [x] Burstiness
- [ ] Span Entropy
- [ ] Memory
- [x] SPAvg : returns switching points. calculate avg over corpus

```
>> from cs_metrics import *
>> sample = 'EN EN HI HI UNIV UNIV HI HI EN EN EN HI HI'
>> cmi(sample)
>> 45.45454545454546 
>> mindex(sample)
>> 0.9836065573770497
>> lang_entropy(sample)
>> 0.9940302114769565
>> burstiness(sample)
>> -0.4835086004775133
```


---
To Dos:
[ ] Take list or str as input.  Implemented for I-index<br>
[ ] case insensitive lang_tags, other_tags. Implemented for I-index<br>
[ ] take num of languages as an input argument<br>
[ ] take num of other tags as an input argument<br>