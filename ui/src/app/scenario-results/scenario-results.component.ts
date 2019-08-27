import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { FormControl, FormGroup } from '@angular/forms';

import { ScenarioResultsService } from './scenario-results.service';
import { ScenarioResults, ResultsButton, ResultsForm } from './scenario-results';

const Bokeh = ( window as any ).require('bokehjs');

@Component({
  selector: 'app-scenario-results',
  templateUrl: './scenario-results.component.html',
  styleUrls: ['./scenario-results.component.css']
})
export class ScenarioResultsComponent implements OnInit {

  // Key for which results table to show
  resultsToShow: string;

  // All results buttons
  allResultsButtons: ResultsButton[];
  // All results forms
  allResultsForms: ResultsForm[];

  // All tables
  allTables: ScenarioResults[];

  // Results tables
  resultsProjectCapacity: ScenarioResults;
  resultsProjectRetirements: ScenarioResults;
  resultsProjectNewBuild: ScenarioResults;
  resultsProjectDispatch: ScenarioResults;
  resultsProjectCarbon: ScenarioResults;
  resultsTransmissionCapacity: ScenarioResults;
  resultsTransmissionFlows: ScenarioResults;
  resultsImportsExports: ScenarioResults;
  resultsSystemLoadBalance: ScenarioResults;
  resultsSystemRPS: ScenarioResults;
  resultsSystemCarbonCap: ScenarioResults;
  resultsSystemPRM: ScenarioResults;

  // Plots
  // Dispatch plot (form with plot options, JSON object, and plot name)
  dispatchPlotOptionsForm = new FormGroup({
    dispatchPlotLoadZone: new FormControl(),
    dispatchPlotHorizon: new FormControl(),
    dispatchPlotYMax: new FormControl()
  });
  dispatchPlotJSON: object;
  dispatchPlotHTMLName: string;

  // Capacity plots (form with plot options, JSON object, and plot name)
  capacityNewPlotOptionsForm = new FormGroup({
    capacityNewPlotLoadZone: new FormControl(),
    capacityNewPlotYMax: new FormControl()
  });
  capacityNewPlotJSON: object;
  capacityNewPlotHTMLName: string;

  capacityRetiredPlotOptionsForm = new FormGroup({
    capacityRetiredPlotLoadZone: new FormControl(),
    capacityRetiredPlotYMax: new FormControl()
  });
  capacityRetiredPlotJSON: object;
  capacityRetiredPlotHTMLName: string;

  capacityTotalPlotOptionsForm = new FormGroup({
    capacityTotalPlotLoadZone: new FormControl(),
    capacityTotalPlotYMax: new FormControl()
  });
  capacityTotalPlotJSON: object;
  capacityTotalPlotHTMLName: string;

  // Energy plot
  energyPlotOptionsForm = new FormGroup({
    energyPlotLoadZone: new FormControl(),
    energyPlotStage: new FormControl(),
    energyPlotYMax: new FormControl()
  });
  energyPlotJSON: object;
  energyPlotHTMLName: string;

  // Cost plot
  costPlotOptionsForm = new FormGroup({
    costPlotLoadZone: new FormControl(),
    costPlotStage: new FormControl(),
    costPlotYMax: new FormControl()
  });
  costPlotJSON: object;
  costPlotHTMLName: string;

  // Capacity factor plot
  capacityFactorPlotOptionsForm = new FormGroup({
    capacityFactorPlotLoadZone: new FormControl(),
    capacityFactorPlotStage: new FormControl(),
    capacityFactorPlotYMax: new FormControl()
  });
  capacityFactorPlotJSON: object;
  capacityFactorPlotHTMLName: string;

  // To get the right route
  scenarioID: number;
  private sub: any;

  constructor(
    private route: ActivatedRoute,
    private scenarioResultsService: ScenarioResultsService,
    private location: Location,

  ) { }

  ngOnInit() {
    console.log('Initializing with results to show', this.resultsToShow);

    // The ActivatedRoute service provides a params Observable which we can
    // subscribe to in order to get the route parameters
    this.sub = this.route.params.subscribe(params => {
       this.scenarioID = +params.id;
       console.log(`Scenario ID is ${this.scenarioID}`);
    });

    // Make the results buttons
    this.allResultsButtons = [];
    this.allResultsForms = [];
    this.makeResultsButtons();
    this.makeResultsForms(this.scenarioID);

    // Initiate the array of all tables
    this.allTables = [];

    // Get the key for which table to show
    this.getResultsToShow();

    // Get data
    if (this.resultsToShow === 'results-project-capacity') {
      this.getResultsProjectCapacity(this.scenarioID);
    }

    if (this.resultsToShow === 'results-project-retirements') {
      this.getResultsProjectRetirements(this.scenarioID);
    }

    if (this.resultsToShow === 'results-project-new-build') {
      this.getResultsProjectNewBuild(this.scenarioID);
    }

    if (this.resultsToShow === 'results-project-dispatch') {
      this.getResultsProjectDispatch(this.scenarioID);
    }

    if (this.resultsToShow === 'results-project-carbon') {
      this.getResultsProjectCarbon(this.scenarioID);
    }

    if (this.resultsToShow === 'results-transmission-capacity') {
      this.getResultsTransmissionCapacity(this.scenarioID);
    }

    if (this.resultsToShow === 'results-transmission-flows') {
      this.getResultsTransmissionFlows(this.scenarioID);
    }

    if (this.resultsToShow === 'results-imports-exports') {
      this.getResultsImportsExports(this.scenarioID);
    }

    if (this.resultsToShow === 'results-system-load-balance') {
      this.getResultsSystemLoadBalance(this.scenarioID);
    }

    if (this.resultsToShow === 'results-system-rps') {
      this.getResultsSystemRPS(this.scenarioID);
    }

    if (this.resultsToShow === 'results-system-carbon-cap') {
      this.getResultsSystemCarbonCap(this.scenarioID);
    }

    if (this.resultsToShow === 'results-system-prm') {
      this.getResultsSystemPRM(this.scenarioID);
    }

    if (this.resultsToShow === 'results-dispatch-plot') {
      console.log('Showing dispatch plot');
      this.getResultsDispatchPlot(this.scenarioID);
    }

    if (this.resultsToShow === 'results-capacity-new-plot') {
      console.log('Showing new capacity plot');
      this.getResultsCapacityNewPlot(this.scenarioID);
    }

    if (this.resultsToShow === 'results-capacity-retired-plot') {
      console.log('Showing retired capacity plot');
      this.getResultsCapacityRetiredPlot(this.scenarioID);
    }

    if (this.resultsToShow === 'results-capacity-total-plot') {
      console.log('Showing total capacity plot');
      this.getResultsCapacityTotalPlot(this.scenarioID);
    }

    if (this.resultsToShow === 'results-energy-plot') {
      console.log('Showing energy plot');
      this.getResultsEnergyPlot(this.scenarioID);
    }

    if (this.resultsToShow === 'results-cost-plot') {
      console.log('Showing cost plot');
      this.getResultsCostPlot(this.scenarioID);
    }

    if (this.resultsToShow === 'results-capacity-factor-plot') {
      console.log('Showing capacity factor plot');
      this.getResultsCapacityFactorPlot(this.scenarioID);
    }
  }

  // Subscribe to the resultsToShow BehaviorSubject, which tells us which
  // results table the user is requesting
  getResultsToShow(): void {
    this.scenarioResultsService.resultsToViewSubject
      .subscribe((resultsToShow: string) => {
        this.resultsToShow = resultsToShow;
      });
  }

  // When a results button is pressed, change the value of resultsToShow to
  // that of the respective results table and refresh the view
  showResults(resultsToShow): void {
    // Send value for show project capacity table
    this.scenarioResultsService.changeResultsToView(resultsToShow);
    // Refresh the view
    this.ngOnInit();
  }


  // Fetch results table subscriptions and add to the allTables arrays
  getResultsProjectCapacity(scenarioID): void {
    this.scenarioResultsService.getResultsProjectCapacity(scenarioID)
      .subscribe(inputTableRows => {
        this.resultsProjectCapacity = inputTableRows;
        this.allTables.push(this.resultsProjectCapacity);
      });
  }

  getResultsProjectRetirements(scenarioID): void {
    this.scenarioResultsService.getResultsProjectRetirements(scenarioID)
      .subscribe(inputTableRows => {
        this.resultsProjectRetirements = inputTableRows;
        this.allTables.push(this.resultsProjectRetirements);
      });
  }

  getResultsProjectNewBuild(scenarioID): void {
    this.scenarioResultsService.getResultsProjectNewBuild(scenarioID)
      .subscribe(inputTableRows => {
        this.resultsProjectNewBuild = inputTableRows;
        this.allTables.push(this.resultsProjectNewBuild);
      });
  }

  getResultsProjectDispatch(scenarioID): void {
    this.scenarioResultsService.getResultsProjectDispatch(scenarioID)
      .subscribe(inputTableRows => {
        this.resultsProjectDispatch = inputTableRows;
        this.allTables.push(this.resultsProjectDispatch);
      });
  }

  getResultsProjectCarbon(scenarioID): void {
    this.scenarioResultsService.getResultsProjectCarbon(scenarioID)
      .subscribe(inputTableRows => {
        this.resultsProjectCarbon = inputTableRows;
        this.allTables.push(this.resultsProjectCarbon);
      });
  }

  getResultsTransmissionCapacity(scenarioID): void {
    this.scenarioResultsService.getResultsTransmissionCapacity(scenarioID)
      .subscribe(inputTableRows => {
        this.resultsTransmissionCapacity = inputTableRows;
        this.allTables.push(this.resultsTransmissionCapacity);
      });
  }

  getResultsTransmissionFlows(scenarioID): void {
    this.scenarioResultsService.getResultsTransmissionFlows(scenarioID)
      .subscribe(inputTableRows => {
        this.resultsTransmissionFlows = inputTableRows;
        this.allTables.push(this.resultsTransmissionFlows);
      });
  }

  getResultsImportsExports(scenarioID): void {
    this.scenarioResultsService.getResultsImportsExports(scenarioID)
      .subscribe(inputTableRows => {
        this.resultsImportsExports = inputTableRows;
        this.allTables.push(this.resultsImportsExports);
      });
  }

  getResultsSystemLoadBalance(scenarioID): void {
    this.scenarioResultsService.getResultsSystemLoadBalance(scenarioID)
      .subscribe(inputTableRows => {
        this.resultsSystemLoadBalance = inputTableRows;
        this.allTables.push(this.resultsSystemLoadBalance);
      });
  }

  getResultsSystemRPS(scenarioID): void {
    this.scenarioResultsService.getResultsSystemRPS(scenarioID)
      .subscribe(inputTableRows => {
        this.resultsSystemRPS = inputTableRows;
        this.allTables.push(this.resultsSystemRPS);
      });
  }

  getResultsSystemCarbonCap(scenarioID): void {
    this.scenarioResultsService.getResultsSystemCarbonCap(scenarioID)
      .subscribe(inputTableRows => {
        this.resultsSystemCarbonCap = inputTableRows;
        this.allTables.push(this.resultsSystemCarbonCap);
      });
  }

  getResultsSystemPRM(scenarioID): void {
    this.scenarioResultsService.getResultsSystemPRM(scenarioID)
      .subscribe(inputTableRows => {
        this.resultsSystemPRM = inputTableRows;
        this.allTables.push(this.resultsSystemPRM);
      });
  }

  getResultsDispatchPlot(scenarioID): void {
    // Get the plot options
    const loadZone = this.dispatchPlotOptionsForm.value.dispatchPlotLoadZone;
    const horizon = this.dispatchPlotOptionsForm.value.dispatchPlotHorizon;
    let yMax = this.dispatchPlotOptionsForm.value.dispatchPlotYMax;
    if (yMax === null) { yMax = 'default'; }

    // Change the plot name for the HTML
    this.dispatchPlotHTMLName = `dispatchPlot-${loadZone}-${horizon}`;

    // Get the JSON object, convert to plot, and embed (the target of the
    // JSON object will match the HTML name above)
    this.scenarioResultsService.getResultsDispatchPlot(
      scenarioID, loadZone, horizon, yMax
    ).subscribe(dispatchPlotAPI => {
        this.dispatchPlotJSON = dispatchPlotAPI.plotJSON;
        Bokeh.embed.embed_item(this.dispatchPlotJSON);
      });
  }

  getResultsCapacityNewPlot(scenarioID): void {
    // Get the plot options
    const loadZone = this.capacityNewPlotOptionsForm.value.capacityNewPlotLoadZone;

    // Change the plot name for the HTML
    this.capacityNewPlotHTMLName = `newCapacityPlot-${loadZone}`;
    let yMax = this.capacityNewPlotOptionsForm.value.capacityNewPlotYMax;
    if (yMax === null) { yMax = 'default'; }

    // Get the JSON object, convert to plot, and embed (the target of the
    // JSON object will match the HTML name above)
    this.scenarioResultsService.getResultsCapacityNewPlot(
      scenarioID, loadZone, yMax
    ).subscribe(plotAPI => {
        this.capacityNewPlotJSON = plotAPI.plotJSON;
        Bokeh.embed.embed_item(this.capacityNewPlotJSON);
      });
  }

  getResultsCapacityRetiredPlot(scenarioID): void {
    // Get the plot options
    const loadZone = this.capacityRetiredPlotOptionsForm.value.capacityRetiredPlotLoadZone;
    let yMax = this.capacityRetiredPlotOptionsForm.value.capacityRetiredPlotYMax;
    if (yMax === null) { yMax = 'default'; }

    // Change the plot name for the HTML
    this.capacityRetiredPlotHTMLName = `retiredCapacityPlot-${loadZone}`;

    // Get the JSON object, convert to plot, and embed (the target of the
    // JSON object will match the HTML name above)
    this.scenarioResultsService.getResultsCapacityRetiredPlot(
      scenarioID, loadZone, yMax
    ).subscribe(plotAPI => {
        this.capacityRetiredPlotJSON = plotAPI.plotJSON;
        Bokeh.embed.embed_item(this.capacityRetiredPlotJSON);
      });
  }

  getResultsCapacityTotalPlot(scenarioID): void {
    // Get the plot options
    const loadZone = this.capacityTotalPlotOptionsForm.value.capacityTotalPlotLoadZone;
    let yMax = this.capacityTotalPlotOptionsForm.value.capacityTotalPlotYMax;
    if (yMax === null) { yMax = 'default'; }

    // Change the plot name for the HTML
    this.capacityTotalPlotHTMLName = `allCapacityPlot-${loadZone}`;

    // Get the JSON object, convert to plot, and embed (the target of the
    // JSON object will match the HTML name above)
    this.scenarioResultsService.getResultsCapacityTotalPlot(
      scenarioID, loadZone, yMax
    ).subscribe(plotAPI => {
        this.capacityTotalPlotJSON = plotAPI.plotJSON;
        Bokeh.embed.embed_item(this.capacityTotalPlotJSON);
      });
  }

  getResultsEnergyPlot(scenarioID): void {
    // Get the plot options
    const loadZone = this.energyPlotOptionsForm.value.energyPlotLoadZone;
    const stage = this.energyPlotOptionsForm.value.energyPlotStage;
    let yMax = this.energyPlotOptionsForm.value.energyPlotYMax;
    if (yMax === null) { yMax = 'default'; }

    // Change the plot name for the HTML
    // TODO: make name 'energyPlot' in python file and here
    this.energyPlotHTMLName = `EnergyPlot-${loadZone}-${stage}`;

    // Get the JSON object, convert to plot, and embed (the target of the
    // JSON object will match the HTML name above)
    this.scenarioResultsService.getResultsEnergyPlot(
      scenarioID, loadZone, stage, yMax
    ).subscribe(energyPlotAPI => {
        this.energyPlotJSON = energyPlotAPI.plotJSON;
        Bokeh.embed.embed_item(this.energyPlotJSON);
      });
  }

  getResultsCostPlot(scenarioID): void {
    // Get the plot options
    const loadZone = this.costPlotOptionsForm.value.costPlotLoadZone;
    const stage = this.costPlotOptionsForm.value.costPlotStage;
    let yMax = this.costPlotOptionsForm.value.costPlotYMax;
    if (yMax === null) { yMax = 'default'; }

    // Change the plot name for the HTML
    // TODO: make name 'costPlot' in python file and here?
    this.costPlotHTMLName = `CostPlot-${loadZone}-${stage}`;

    // Get the JSON object, convert to plot, and embed (the target of the
    // JSON object will match the HTML name above)
    this.scenarioResultsService.getResultsCostPlot(
      scenarioID, loadZone, stage, yMax
    ).subscribe(costPlotAPI => {
        this.costPlotJSON = costPlotAPI.plotJSON;
        Bokeh.embed.embed_item(this.costPlotJSON);
      });
  }

  getResultsCapacityFactorPlot(scenarioID): void {
    // Get the plot options
    const loadZone = this.capacityFactorPlotOptionsForm.value.capacityFactorPlotLoadZone;
    const stage = this.capacityFactorPlotOptionsForm.value.capacityFactorPlotStage;
    let yMax = this.capacityFactorPlotOptionsForm.value.capacityFactorPlotYMax;
    if (yMax === null) { yMax = 'default'; }

    // Change the plot name for the HTML
    // TODO: make name 'capFactorPlot' in python file and here?
    this.capacityFactorPlotHTMLName = `CapFactorPlot-${loadZone}-${stage}`;

    // Get the JSON object, convert to plot, and embed (the target of the
    // JSON object will match the HTML name above)
    this.scenarioResultsService.getResultsCapacityFactorPlot(
      scenarioID, loadZone, stage, yMax
    ).subscribe(capacityFactorPlotAPI => {
        this.capacityFactorPlotJSON = capacityFactorPlotAPI.plotJSON;
        Bokeh.embed.embed_item(this.capacityFactorPlotJSON);
      });
  }

  // Make the results buttons with their relevant keys that are passed to
  // the resultsToViewSubject in scenario-results.service.ts
  makeResultsButtons(): void {
    const projectCapacityButton = {
      name: 'showResultsProjectCapacityButton',
      ngIfKey: 'results-project-capacity',
      caption: 'Project Capacity'
    };
    this.allResultsButtons.push(projectCapacityButton);

    const projectRetirementsButton = {
      name: 'showResultsProjectRetirementsButton',
      ngIfKey: 'results-project-retirements',
      caption: 'Project Retirements'
    };
    this.allResultsButtons.push(projectRetirementsButton);

    const projectNewBuildButton = {
      name: 'showResultsProjectNewBuildButton',
      ngIfKey: 'results-project-new-build',
      caption: 'Project New Build'
    };
    this.allResultsButtons.push(projectNewBuildButton);

    const projectDispatchButton = {
      name: 'showResultsProjectDispatchButton',
      ngIfKey: 'results-project-dispatch',
      caption: 'Project Dispatch'
    };
    this.allResultsButtons.push(projectDispatchButton);

    const projectCarbonButton = {
      name: 'showResultsProjectCarbonButton',
      ngIfKey: 'results-project-carbon',
      caption: 'Project Carbon'
    };
    this.allResultsButtons.push(projectCarbonButton);

    const transmissionCapacityButton = {
      name: 'showResultsTransmissionCapacityButton',
      ngIfKey: 'results-transmission-capacity',
      caption: 'Transmission Capacity'
    };
    this.allResultsButtons.push(transmissionCapacityButton);

    const transmissionFlowsButton = {
      name: 'showResultsTransmissionFlowsButton',
      ngIfKey: 'results-transmission-flows',
      caption: 'Transmission Flows'
    };
    this.allResultsButtons.push(transmissionFlowsButton);

    const importsExportsButton = {
      name: 'showResultsImportsExportsButton',
      ngIfKey: 'results-imports-exports',
      caption: 'Imports/Exports'
    };
    this.allResultsButtons.push(importsExportsButton);

    const systemLoadBalanceButton = {
      name: 'showResultsSystemLoadBalanceButton',
      ngIfKey: 'results-system-load-balance',
      caption: 'Load Balance'
    };
    this.allResultsButtons.push(systemLoadBalanceButton);

    const systemRPSButton = {
      name: 'showResultsSystemRPSButton',
      ngIfKey: 'results-system-rps',
      caption: 'RPS'
    };
    this.allResultsButtons.push(systemRPSButton);

    const systemCarbonCapButton = {
      name: 'showResultsSystemCarbonCapButton',
      ngIfKey: 'results-system-carbon-cap',
      caption: 'Carbon Cap'
    };
    this.allResultsButtons.push(systemCarbonCapButton);

    const systemPRMButton = {
      name: 'showResultsSystemPRMButton',
      ngIfKey: 'results-system-prm',
      caption: 'PRM'
    };
    this.allResultsButtons.push(systemPRMButton);
  }

  makeResultsForms(scenarioID): void {
    this.scenarioResultsService.getOptions(scenarioID).subscribe(
      plotOptions => {
        const dispatchPlotFormStructure = {
          formGroup: this.dispatchPlotOptionsForm,
          selectForms: [
            {formControlName: 'dispatchPlotLoadZone',
             formControlOptions: plotOptions.loadZoneOptions},
            {formControlName: 'dispatchPlotHorizon',
            formControlOptions: plotOptions.horizonOptions}
          ],
          yMaxFormControlName: 'dispatchPlotYMax',
          button: {
            name: 'showResultsDispatchPlotButton',
            ngIfKey: 'results-dispatch-plot',
            caption: 'System Dispatch'
          }
        };
        this.allResultsForms.push(dispatchPlotFormStructure);

        const plotCapNewFormStructure = {
          formGroup: this.capacityNewPlotOptionsForm,
          selectForms: [
            {formControlName: 'capacityNewPlotLoadZone',
             formControlOptions: plotOptions.loadZoneOptions}
          ],
          yMaxFormControlName: 'capacityNewPlotYMax',
          button: {
            name: 'showResultsCapacityNewPlotButton',
            ngIfKey: 'results-capacity-new-plot',
            caption: 'New Capacity'
          }
        };
        this.allResultsForms.push(plotCapNewFormStructure);

        const plotCapRetiredFormStructure = {
          formGroup: this.capacityRetiredPlotOptionsForm,
          selectForms: [
            {formControlName: 'capacityRetiredPlotLoadZone',
             formControlOptions: plotOptions.loadZoneOptions}
          ],
          yMaxFormControlName: 'capacityRetiredPlotYMax',
          button: {
            name: 'showResultsCapacityRetiredPlotButton',
            ngIfKey: 'results-capacity-retired-plot',
            caption: 'Retired Capacity'
          }
        };
        this.allResultsForms.push(plotCapRetiredFormStructure);

        const plotCapTotalFormStructure = {
          formGroup: this.capacityTotalPlotOptionsForm,
          selectForms: [
            {formControlName: 'capacityTotalPlotLoadZone',
             formControlOptions: plotOptions.loadZoneOptions}
          ],
          yMaxFormControlName: 'capacityTotalPlotYMax',
          button: {
            name: 'showResultsCapacityTotalPlotButton',
            ngIfKey: 'results-capacity-total-plot',
            caption: 'Total Capacity'
          }
        };
        this.allResultsForms.push(plotCapTotalFormStructure);

        const energyPlotFormStructure = {
          formGroup: this.energyPlotOptionsForm,
          selectForms: [
            {formControlName: 'energyPlotLoadZone',
             formControlOptions: plotOptions.loadZoneOptions},
            {formControlName: 'energyPlotStage',
            formControlOptions: plotOptions.stageOptions}
          ],
          yMaxFormControlName: 'energyPlotYMax',
          button: {
            name: 'showResultsEnergyPlotButton',
            ngIfKey: 'results-energy-plot',
            caption: 'System Energy Mix'
          }
        };
        this.allResultsForms.push(energyPlotFormStructure);

        const costPlotFormStructure = {
          formGroup: this.costPlotOptionsForm,
          selectForms: [
            {formControlName: 'costPlotLoadZone',
             formControlOptions: plotOptions.loadZoneOptions},
            {formControlName: 'costPlotStage',
            formControlOptions: plotOptions.stageOptions}
          ],
          yMaxFormControlName: 'costPlotYMax',
          button: {
            name: 'showResultsCostPlotButton',
            ngIfKey: 'results-cost-plot',
            caption: 'System Cost'
          }
        };
        this.allResultsForms.push(costPlotFormStructure);

        const capacityFactorPlotFormStructure = {
          formGroup: this.capacityFactorPlotOptionsForm,
          selectForms: [
            {formControlName: 'capacityFactorPlotLoadZone',
             formControlOptions: plotOptions.loadZoneOptions},
            {formControlName: 'capacityFactorPlotStage',
            formControlOptions: plotOptions.stageOptions}
          ],
          yMaxFormControlName: 'capacityFactorPlotYMax',
          button: {
            name: 'showResultsCapacityFactorPlotButton',
            ngIfKey: 'results-capacity-factor-plot',
            caption: 'Capacity Factors'
          }
        };
        this.allResultsForms.push(capacityFactorPlotFormStructure);

      }
    );
  }

  goBack(): void {
    this.location.back();
    // The the resultsToView to '', so that we start with no tables visible
    // when we visit the results page again
    this.scenarioResultsService.changeResultsToView('');
  }

}
