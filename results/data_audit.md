# Controllo dei dati

Generato da `scripts/audit_data.py`. Non modificare a mano: rilancia lo script.

## Riepilogo

| Dataset | Requisito | Esito |
| --- | --- | --- |
| telco (WA_Fn-UseC_-Telco-Customer-Churn.csv) | Target churn binario (RQ1-RQ3) | OK |
| telco (WA_Fn-UseC_-Telco-Customer-Churn.csv) | Durata per la survival (RQ4) | OK |
| iranian (Customer Churn.csv) | Target churn binario (RQ1-RQ3) | OK |
| iranian (Customer Churn.csv) | Durata per la survival (RQ4) | OK |
| cell2cell (cell2cellholdout.csv) | Target churn binario (RQ1-RQ3) | SENZA ETICHETTA (file di test, non usabile per addestrare) |
| cell2cell (cell2cellholdout.csv) | Durata per la survival (RQ4) | OK |
| cell2cell (cell2celltrain.csv) | Target churn binario (RQ1-RQ3) | OK |
| cell2cell (cell2celltrain.csv) | Durata per la survival (RQ4) | OK |
| hillstrom (hillstorm_no_indices.csv) | Trattamento + esito per l'uplift (RQ5) | OK |
| criteo | File presenti | FACOLTATIVO, non scaricato |

## Dettaglio per file

### telco – `telco\WA_Fn-UseC_-Telco-Customer-Churn.csv`

- Righe: **7.043**, colonne: **21**
- Valori mancanti: nessuno
- Celle con solo spazi (sono mancanti nascosti): `TotalCharges`
- Righe duplicate: 0
- Target `Churn`: No: 73,5%, Yes: 26,5%
- Righe con etichetta: 7.043 su 7.043
- Durata `tenure`: da 0 a 72, mediana 29
- Colonne: `customerID`, `gender`, `SeniorCitizen`, `Partner`, `Dependents`, `tenure`, `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`, `Contract`, `PaperlessBilling`, `PaymentMethod`, `MonthlyCharges`, `TotalCharges`, `Churn`

### iranian – `iranian\Customer Churn.csv`

- Righe: **3.150**, colonne: **14**
- Valori mancanti: nessuno
- Righe duplicate: 300
- Target `Churn`: 0: 84,3%, 1: 15,7%
- Righe con etichetta: 3.150 su 3.150
- Durata `Subscription  Length`: da 3 a 47, mediana 35
- Colonne: `Call  Failure`, `Complains`, `Subscription  Length`, `Charge  Amount`, `Seconds of Use`, `Frequency of use`, `Frequency of SMS`, `Distinct Called Numbers`, `Age Group`, `Tariff Plan`, `Status`, `Age`, `Customer Value`, `Churn`

### cell2cell – `cell2cell\cell2cellholdout.csv`

- Righe: **20.000**, colonne: **58**
- Valori mancanti in 12 colonne; le principali: `Churn` (20000), `AgeHH1` (335), `AgeHH2` (335), `PercChangeMinutes` (135), `PercChangeRevenues` (135)
- Righe duplicate: 0
- Target `Churn`: 
- Righe con etichetta: 0 su 20.000
- Durata `MonthsInService`: da 6 a 61, mediana 16
- Colonne: `CustomerID`, `Churn`, `MonthlyRevenue`, `MonthlyMinutes`, `TotalRecurringCharge`, `DirectorAssistedCalls`, `OverageMinutes`, `RoamingCalls`, `PercChangeMinutes`, `PercChangeRevenues`, `DroppedCalls`, `BlockedCalls`, `UnansweredCalls`, `CustomerCareCalls`, `ThreewayCalls`, `ReceivedCalls`, `OutboundCalls`, `InboundCalls`, `PeakCallsInOut`, `OffPeakCallsInOut`, `DroppedBlockedCalls`, `CallForwardingCalls`, `CallWaitingCalls`, `MonthsInService`, `UniqueSubs`, `ActiveSubs`, `ServiceArea`, `Handsets`, `HandsetModels`, `CurrentEquipmentDays`, `AgeHH1`, `AgeHH2`, `ChildrenInHH`, `HandsetRefurbished`, `HandsetWebCapable`, `TruckOwner`, `RVOwner`, `Homeownership`, `BuysViaMailOrder`, `RespondsToMailOffers`, `OptOutMailings`, `NonUSTravel`, `OwnsComputer`, `HasCreditCard`, `RetentionCalls`, `RetentionOffersAccepted`, `NewCellphoneUser`, `NotNewCellphoneUser`, `ReferralsMadeBySubscriber`, `IncomeGroup`, `OwnsMotorcycle`, `AdjustmentsToCreditRating`, `HandsetPrice`, `MadeCallToRetentionTeam`, `CreditRating`, `PrizmCode`, `Occupation`, `MaritalStatus`

### cell2cell – `cell2cell\cell2celltrain.csv`

- Righe: **51.047**, colonne: **58**
- Valori mancanti in 14 colonne; le principali: `AgeHH2` (909), `AgeHH1` (909), `PercChangeRevenues` (367), `PercChangeMinutes` (367), `MonthlyRevenue` (156)
- Righe duplicate: 0
- Target `Churn`: No: 71,2%, Yes: 28,8%
- Righe con etichetta: 51.047 su 51.047
- Durata `MonthsInService`: da 6 a 61, mediana 16
- Colonne: `CustomerID`, `Churn`, `MonthlyRevenue`, `MonthlyMinutes`, `TotalRecurringCharge`, `DirectorAssistedCalls`, `OverageMinutes`, `RoamingCalls`, `PercChangeMinutes`, `PercChangeRevenues`, `DroppedCalls`, `BlockedCalls`, `UnansweredCalls`, `CustomerCareCalls`, `ThreewayCalls`, `ReceivedCalls`, `OutboundCalls`, `InboundCalls`, `PeakCallsInOut`, `OffPeakCallsInOut`, `DroppedBlockedCalls`, `CallForwardingCalls`, `CallWaitingCalls`, `MonthsInService`, `UniqueSubs`, `ActiveSubs`, `ServiceArea`, `Handsets`, `HandsetModels`, `CurrentEquipmentDays`, `AgeHH1`, `AgeHH2`, `ChildrenInHH`, `HandsetRefurbished`, `HandsetWebCapable`, `TruckOwner`, `RVOwner`, `Homeownership`, `BuysViaMailOrder`, `RespondsToMailOffers`, `OptOutMailings`, `NonUSTravel`, `OwnsComputer`, `HasCreditCard`, `RetentionCalls`, `RetentionOffersAccepted`, `NewCellphoneUser`, `NotNewCellphoneUser`, `ReferralsMadeBySubscriber`, `IncomeGroup`, `OwnsMotorcycle`, `AdjustmentsToCreditRating`, `HandsetPrice`, `MadeCallToRetentionTeam`, `CreditRating`, `PrizmCode`, `Occupation`, `MaritalStatus`

### hillstrom – `hillstrom\hillstorm_no_indices.csv`

- Righe: **64.000**, colonne: **12**
- Valori mancanti: nessuno
- Righe duplicate: 6562
- Trattamento `segment`: Womens E-Mail: 33,4%, Mens E-Mail: 33,3%, No E-Mail: 33,3%
- Esito `visit`: media 14,7%
- Esito `conversion`: media 0,9%
- Esito `spend`: media 1.05
- Colonne: `recency`, `history_segment`, `history`, `mens`, `womens`, `zip_code`, `newbie`, `channel`, `segment`, `visit`, `conversion`, `spend`

### criteo

- Non scaricato (facoltativo)
