import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent {

  @Input() response: {
    original_email: string,
    suggestions: Array<{
      original_sentence: string,
      improved_sentence: string,
    }>
  } | null = null;


}
