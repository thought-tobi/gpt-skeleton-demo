import { Component } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {lastValueFrom} from "rxjs";


@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.css']
})
export class InputComponent {

  email: string = '';
  inputDone: boolean = false;
  response: any | null = null;

  constructor(private http: HttpClient) {}

  async checkEmail() {
    this.inputDone = true;
    await this.sendToBackend(this.email);
  }

  async sendToBackend(email: string) {
    const backend = 'http://localhost:5000/check';
    const data = btoa(email)
    console.log(data)
    const response$ = this.http.post(backend, data);
    this.response = await lastValueFrom(response$)
  }
}
