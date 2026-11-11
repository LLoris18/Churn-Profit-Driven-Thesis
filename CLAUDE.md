# CLAUDE.md — Tesi magistrale: churn prediction profit-driven

Questo file raccoglie il contesto del progetto di tesi. Va letto all'inizio di ogni sessione,
in chat con Claude o con Claude Code, e aggiornato quando si prende una decisione.
Ultimo aggiornamento: 2026-11-11.

**Documento di riferimento:** la pagina Notion "🎓 Tesi – Documento unico" (vedi §16).
Questo file è la versione sintetica per Claude Code; se i due divergono, vale Notion.

---

## 1. In una frase

Tesi sperimentale in Python che verifica se scegliere un modello di churn in base al
**profitto** (EMPC) invece che all'**accuratezza/AUC** porta a decisioni di retention diverse
e migliori. L'analisi si estende a **quando** intervenire (survival analysis) e **con quale
azione** (SHAP + LLM, uplift modeling).

## 2. Persone e contesto

- **Studente:** Loris Garzarella, Laurea Magistrale in Ingegneria Gestionale, Politecnico di Bari
  (DMMM, percorso Imprenditorialità e Innovazione). Lavora full-time come Production Manager:
  tempo disponibile circa 8-10 ore a settimana.
- **Relatore:** Prof. Umberto Panniello (corso "Modelli di E-Business e Business Intelligence", MEBI).
- **Correlatore / co-supervisore:** Ing. Foggetti.
- **Livello di partenza:** basi di Python, neofita di data mining e machine learning.
  Obiettivo personale: imparare davvero, e usare la tesi come progetto di portfolio per ruoli
  data science / AI in Nord Europa o a Londra.

## 3. Stato e cronologia

- 2026-10-08: prima mail al professore per chiedere la tesi su data mining.
- 2026-10-09: proposta inviata (churn profit-driven, paper di Verbeke e Baesens).
- 2026-10-13: il professore accetta il tema. Chiede: titolo provvisorio, abstract breve
  (obiettivo + metodologia), indice provvisorio. Ing. Foggetti in copia come co-supervisore.
- 2026-10-22: preparati titolo/abstract/indice, doc di teoria, doc di risorse, questo file.
- 2026-10-28: relatore e correlatore approvano tema e dataset; consigliano di partire dalla
  raccolta dei dati.
- 2026-11-05: `download_data.py` con fonti di riserva per Hillstrom ed estrazione automatica
  degli zip; token Kaggle nuovo formato (`~/.kaggle/access_token` o `KAGGLE_API_TOKEN`).
- 2026-11-11: **Fase 0 (raccolta dati) chiusa.** Tutti i dataset scaricati e controllati con
  `audit_data.py`; tutti i requisiti delle RQ sono soddisfatti (dettagli in §8).
- **Prossimo passo:** rilanciare `download_data.py` (versione 5 nov) per aggiornare il manifest,
  backup di `data/raw/`, commit, bozza del §4.1 Dataset, breve mail ai relatori, poi
  notebook `01_eda` sul Telco.

## 4. Vincoli (non negoziabili)

- **Solo dati pubblici o sintetici dichiarati.** Vietato usare dati dell'azienda in cui lavora
  lo studente (nessun dato ERP, produzione o macchine).
- **Python, non WEKA.** Le tecniche del corso vanno replicate in Python.
- **Riproducibilità:** codice su GitHub, dati scaricati da script e mai caricati nel repo, seed fissati.
- **Uso dell'AI dichiarato** nella tesi, secondo le indicazioni del relatore (da chiedere).
- Lingua della tesi: italiano o inglese, **da confermare** con il relatore (preferenza: inglese).

## 5. Titolo, obiettivo e domande di ricerca

**Titolo provvisorio:** "Dall'accuratezza al profitto: modelli di churn prediction profit-driven
per decidere quali clienti trattenere, quando e con quale azione"
(EN: "From Accuracy to Profit: Profit-Driven Churn Prediction to Decide Whom to Retain, When and How").

**Domande di ricerca (bozza):**

- RQ1 — Chi contattare: la classifica dei modelli per AUC coincide con quella per EMPC?
  Quanto profitto si perde scegliendo il modello per AUC?
- RQ2 — Sbilanciamento: con modelli forti (gradient boosting), SMOTE migliora il profitto
  rispetto a pesi cost-sensitive o alla sola ottimizzazione della soglia?
- RQ3 — Interpretabilità: quanto profitto si perde con un albero poco profondo (3-5 livelli)
  rispetto al miglior ensemble?
- RQ4 — Quando: la survival analysis identifica una finestra di intervento utile per i clienti a rischio?
- RQ5 — Quale azione: un LLM che traduce i fattori di rischio (SHAP) in azioni produce un
  profitto simulato maggiore di una regola unica uguale per tutti? Come si confronta con
  l'uplift modeling su dati sperimentali (Hillstrom)?
- (facoltativa) Le feature generate da un LLM (stile CAAFE) aumentano l'EMPC fuori campione?

Anche un risultato negativo, misurato bene, è un contributo valido.

## 6. Indice provvisorio

Introduzione · 1 Customer retention e churn management · 2 BI e data mining per la churn
prediction · 3 Dalla previsione alla decisione: stato dell'arte · 4 Metodologia ·
5 Risultati: quali clienti contattare · 6 Risultati: quando intervenire ·
7 Risultati: con quale azione · 8 Discussione · Conclusioni · Bibliografia · Appendici.

## 7. Metodologia (sintesi)

1. **Business understanding:** parametri economici della campagna (CLV, costo contatto,
   costo incentivo, tasso di accettazione) + analisi di sensibilità.
2. **Data preparation:** valori mancanti, encoding one-hot, normalizzazione, split stratificato,
   tutto dentro una `sklearn.pipeline.Pipeline` per evitare data leakage.
3. **Data exploration:** univariata e bivariata, churner vs fedeli (come nel corso).
4. **Modelli:** regressione logistica, albero di decisione (baseline del corso), random forest,
   XGBoost/LightGBM; facoltativi TabPFN e modelli profit-driven di Empulse.
5. **Valutazione classica:** cross-validation stratificata ripetuta, confusion matrix, ROC/AUC,
   gain e lift chart, Brier score.
6. **Valutazione in profitto:** EMPC e MPC (Empulse), frazione ottimale da contattare, curve di profitto.
7. **Quando:** Kaplan-Meier, modello di Cox, C-index (lifelines) su `tenure` del Telco.
8. **Quale azione:** SHAP per i motivi del rischio → LLM che sceglie l'azione da un catalogo →
   simulazione del profitto con ipotesi dichiarate; uplift (T/S/X-learner, curva Qini) su Hillstrom.
9. **Test statistici:** Wilcoxon, t-test corretto di Nadeau-Bengio, Friedman/Nemenyi, bootstrap,
   correlazione di Spearman tra classifiche.

**Parametri EMPC di default (Empulse):** CLV = 200, costo incentivo = 10, costo contatto = 1,
accettazione γ ~ Beta(6, 14). Il churner va codificato come 1.

## 8. Dataset

Dati controllati l'11/11/2026 (`results/data_audit.md`, `results/data_manifest.json`).

| Dataset | Ruolo | File | Righe × colonne | Target / esito | Durata |
| --- | --- | --- | --- | --- | --- |
| IBM Telco (Kaggle, blastchar) | Caso principale | `WA_Fn-UseC_-Telco-Customer-Churn.csv` | 7.043 × 21 | `Churn` Yes 26,5% | `tenure` 0-72 mesi, mediana 29 |
| Iranian Churn (UCI 563) | Controllo, piccolo | `Customer Churn.csv` | 3.150 × 14 (300 duplicati) | `Churn` 1 = 15,7% | `Subscription  Length` 3-47, mediana 35 |
| Cell2Cell (Kaggle, jpacse) | Controllo, il più grande | `cell2celltrain.csv` | 51.047 × 58 | `Churn` Yes 28,8% | `MonthsInService` 6-61, mediana 16 |
| Cell2Cell holdout | **Non usato** | `cell2cellholdout.csv` | 20.000 × 58 | `Churn` vuoto in tutte le righe | — |
| Hillstrom MineThatData | Uplift | `hillstorm_no_indices.csv` (da .csv.gz) | 64.000 × 12 | `segment` 3 bracci ~33%; `visit` 14,7%, `conversion` 0,9%, `spend` media 1,05 | — |
| Criteo Uplift | Eventuale test di scala | non scaricato | ~14 M | CC BY-NC-SA 4.0 | — |

KKBox escluso: la licenza della competizione non ne consente più l'uso.

**Regole di preparazione decise (2026-11-11):**

- Telco: `TotalCharges` ha celle con solo spazi (clienti con `tenure` = 0) → convertire in numero,
  imputare 0 o eliminare le righe (decisione da documentare). `customerID` non è una feature.
- Iranian: eliminare i 300 duplicati **prima** dello split; verificare `Status` per possibile leakage;
  `Age` e `Age Group` sono ridondanti (tenerne una). Non adatto alla survival (durata troncata).
  `Customer Value` utilizzabile come CLV per cliente nell'EMPC (idea da valutare).
- Cell2Cell: usare solo il train; valori mancanti in 14 colonne (AgeHH1/2 909, PercChange* 367,
  MonthlyRevenue 156) → imputazione dentro la Pipeline; `RetentionCalls`,
  `RetentionOffersAccepted`, `MadeCallToRetentionTeam` da verificare per leakage;
  `MonthsInService` parte da 6 (troncamento a sinistra) → survival solo approssimata.
- Hillstrom: i 6.562 duplicati sono attesi (poche feature categoriche) e si tengono;
  esito principale `visit`; confronto principale Womens E-Mail vs No E-Mail.
- Survival (RQ4): Telco principale, Cell2Cell come controllo approssimato, non Iranian.

Licenze di Telco e Cell2Cell da verificare prima della consegna.
Struttura completa e dizionario delle variabili: pagina Notion "Dataset".

## 9. Struttura del repository (proposta)

```
churn-profit-thesis/
├── CLAUDE.md               # questo file
├── README.md               # problema, risultato principale, come riprodurre (in inglese)
├── pyproject.toml          # dipendenze (uv)
├── configs/                # YAML: dataset, modelli, parametri economici
├── data/                   # NON versionata: raw/, processed/ + README con le licenze
├── scripts/                # download_data.py, run_experiment.py, make_figures.py
├── src/churnprofit/        # data.py, features.py, models.py, metrics.py, survival.py, uplift.py, llm.py
├── notebooks/              # 01_eda, 02_baselines, 03_profit, 04_survival, 05_actions (solo racconto)
├── prompts/                # prompt LLM versionati
├── results/                # metriche (CSV/JSON), log delle chiamate LLM (JSONL)
├── figures/                # grafici esportati in PDF/SVG per la tesi
├── tests/                  # pytest: split temporali, metriche, assenza di leakage
└── thesis/                 # sorgenti LaTeX (Overleaf) o collegamento
```

## 10. Convenzioni di codice

- Python 3.11+, ambiente gestito con `uv`; dipendenze bloccate.
- Codice e nomi di variabili in inglese; commenti brevi in inglese.
- La logica vive in `src/`; i notebook importano da lì e servono solo a raccontare.
- `random_state` / seed fissati ovunque (default 42).
- Ogni numero o grafico della tesi deve essere rigenerabile da uno script.
- Nessuna chiave API nel codice: usare variabili d'ambiente (`ANTHROPIC_API_KEY`) e `.env` in `.gitignore`.
- Formattazione e lint con `ruff`; test con `pytest`.

## 11. Regole per l'uso degli LLM negli esperimenti

- Identificativo esatto del modello fissato in `configs/`; temperatura 0.
- Ogni prompt e ogni risposta salvati in `results/llm_logs/*.jsonl` con data, modello, parametri.
- Output strutturato in JSON con schema fisso, validato prima dell'uso.
- L'LLM vede solo informazioni del training set (niente leakage).
- Esperimento principale ripetuto con un modello open locale via Ollama.
- Budget API dichiarato e monitorato.

## 12. Come deve comportarsi Claude in questo progetto

- Lo studente è principiante: **spiega ogni passaggio** in parole semplici, in italiano, prima o
  insieme al codice. L'obiettivo è che sappia rifare e difendere ogni scelta in discussione.
- Non scrivere tutto in un colpo: procedi per piccoli passi verificabili e chiedi conferma sulle
  scelte metodologiche importanti.
- Segnala sempre i rischi di **data leakage**, overfitting e risultati "troppo belli"
  (per esempio accuratezza > 95% sul churn).
- Collega quando possibile le tecniche alle **sbobinature MEBI 2018** (pagine indicate nel doc di teoria).
- Non usare né suggerire dati aziendali dello studente.
- Quando si prende una decisione, proponi di aggiornare la sezione "Registro decisioni" qui sotto.

## 13. Registro decisioni

| Data | Decisione | Motivo |
| --- | --- | --- |
| 2026-10-09 | Tema: churn profit-driven (preferito all'idea del lancio di nuovi prodotti) | Verifica oggettiva sui dati, vicino al corso e al relatore, letteratura solida |
| 2026-10-09 | Estensione: quando intervenire e con quale azione | Richiesta dello studente; collegata a "Beyond customer churn" del relatore |
| 2026-10-09 | Nessun vincolo di laurea ad aprile: tempo stimato circa 8 mesi | Qualità della tesi prioritaria |
| 2026-10-09 | LLM: Claude via API per gli esperimenti + replica con modello open locale | Riproducibilità |
| 2026-10-22 | Proposta al relatore in due versioni: A completa (chi, quando, quale azione); B ridotta (chi + azione con SHAP/LLM e simulazione; survival e uplift come sviluppi futuri) | Avere un piano di riserva se il tempo non basta |
| 2026-10-23 | Dataset: Telco (principale), Iranian e Cell2Cell (controllo), Hillstrom (uplift), Criteo (eventuale test di scala); KKBox escluso | Licenza KKBox scaduta |
| 2026-10-28 | Relatori approvano; si parte dalla raccolta dati | Indicazione del relatore |
| 2026-11-05 | Notion come documento unico di riferimento | I doc separati non si esportavano insieme |
| 2026-11-05 | Token Kaggle in `~/.kaggle/access_token` o `KAGGLE_API_TOKEN`, mai nel repo | Sicurezza |
| 2026-11-11 | Cell2Cell: solo `cell2celltrain.csv` | L'holdout non ha etichette |
| 2026-11-11 | Iranian: rimozione dei 300 duplicati prima dello split | Evitare che lo stesso cliente finisca in train e test |
| 2026-11-11 | Hillstrom: duplicati tenuti, esito principale `visit` | Duplicati attesi; `conversion` troppo rara (0,9%) |
| 2026-11-11 | Survival su Telco (e Cell2Cell approssimata), non su Iranian | Qualità della variabile di durata |

## 14. Domande aperte per il relatore

- [ ] Tesi in inglese?
- [ ] Pubblicazione del codice su GitHub?
- [ ] Stile delle citazioni e template LaTeX
- [ ] Come dichiarare l'uso dell'AI
- [ ] Frequenza e forma degli aggiornamenti
- [ ] Preferenza tra modello LLM commerciale via API e modello open locale

## 15. Letteratura chiave

- Verbeke, Dejaeger, Martens, Hur, Baesens (2012). New insights into churn prediction in the
  telecommunication sector: A profit driven data mining approach. EJOR 218(1), 211-229.
- Verbraken, Verbeke, Baesens (2013). A novel profit maximizing metric for measuring classification
  performance of customer churn prediction models. IEEE TKDE. doi:10.1109/TKDE.2012.50
- Gorgoglione, Panniello (2011). Beyond Customer Churn: Generating Personalized Actions to Retain
  Customers in a Retail Bank by a Recommender System Approach. JILSA 3(2).
- Neslin, Gupta, Kamakura, Lu, Mason (2006). Defection Detection. Journal of Marketing Research 43(2).
- Ascarza (2018). Retention Futility. Journal of Marketing Research. doi:10.1509/jmr.16.0163
- Devriendt, Berrevoets, Verbeke (2021). Why you should stop predicting customer churn and start
  using uplift models. Information Sciences.
- Van den Poel, Larivière (2004). Customer attrition analysis for financial services using
  proportional hazard models. EJOR 157(1).
- Elor, Averbuch-Elor (2022). To SMOTE, or not to SMOTE? arXiv:2201.08528
- Hollmann, Müller, Hutter (2023). CAAFE. NeurIPS.
- Demšar (2006). Statistical Comparisons of Classifiers over Multiple Data Sets. JMLR 7.
- Provost, Fawcett (2013). Data Science for Business, cap. 7-8.
- Verbeke, Baesens, Bravo (2017). Profit-Driven Business Analytics. Wiley.

## 16. Documenti collegati

**Riferimento unico (Notion):** "🎓 Tesi – Documento unico"
https://app.notion.com/p/407c1b5fc284814b93eefd588c143940
Sottopagine: Proposta, Roadmap, Teoria, Letteratura, Risorse, Dataset.

I vecchi documenti su claude.ai (Proposta, Teoria, Risorse, Roadmap, Preparazione call)
sono superati e non vengono più aggiornati.

- Materiale del corso: Sbobinature MEBI 2018 (PDF, 133 pagine)
