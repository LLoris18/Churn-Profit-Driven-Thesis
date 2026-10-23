# CLAUDE.md — Tesi magistrale: churn prediction profit-driven

Questo file raccoglie il contesto del progetto di tesi. Va letto all'inizio di ogni sessione,
in chat con Claude o con Claude Code, e aggiornato quando si prende una decisione.
Ultimo aggiornamento: 2026-10-22.

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
- **Prossimo passo:** inviare titolo, abstract e indice a Panniello e Foggetti; iniziare la
  fase 1 della roadmap (Python e pandas sul dataset Telco).

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

| Dataset | Ruolo | Note |
| --- | --- | --- |
| IBM Telco Customer Churn (Kaggle, blastchar) | Caso principale | 7.043 clienti, colonna `tenure` per la survival |
| Iranian Churn (UCI 563) | Controllo | 3.150 clienti, 495 churner |
| KKBox Churn (Kaggle competition) | Estensione temporale | File pesanti: campionare, usare DuckDB/polars |
| Cell2Cell (Kaggle) | Alternativa a KKBox | Da verificare |
| Hillstrom MineThatData (`sklift.datasets.fetch_hillstrom`) | Uplift | Esperimento randomizzato, 64.000 clienti |

Licenze di Telco, KKBox e Cell2Cell da verificare prima della consegna.

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

## 16. Documenti collegati (claude.ai)

- Proposta di tesi (titolo, abstract, indice): https://claude.ai/artifact/HW21xDirnjNCPHkr9nJbYe
- Teoria per la tesi: https://claude.ai/artifact/3ez5Wdg6zkHKwEvQrCq4Qi
- Risorse (dataset, documentazione, scrittura): https://claude.ai/artifact/3yGi1D117qGkArRhyoLpaL
- Roadmap della tesi (da oggi alla consegna): https://claude.ai/artifact/5iapjQCTTsVRibtvF3ATRR
- Preparazione call (prima versione della roadmap): https://claude.ai/code/artifact/4549ccfe-cbf3-424d-b4b3-44660d5e4d64
- Materiale del corso: Sbobinature MEBI 2018 (PDF, 133 pagine)
